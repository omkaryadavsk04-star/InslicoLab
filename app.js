const ATOMIC_WEIGHTS = {
  C: 12.011,
  H: 1.008,
  N: 14.007,
  O: 15.999,
  S: 32.06,
  P: 30.974,
  F: 18.998,
  Cl: 35.45,
  Br: 79.904,
  I: 126.904,
};

const examples = [
  { name: "Aspirin", smiles: "CC(=O)OC1=CC=CC=C1C(=O)O" },
  { name: "Caffeine", smiles: "Cn1cnc2c1c(=O)n(C)c(=O)n2C" },
  { name: "Ibuprofen", smiles: "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O" },
];

let library = [];
const API_URL =
  window.location.protocol === "file:" ? "http://127.0.0.1:8000/api/analyze" : `${window.location.origin}/api/analyze`;

const form = document.querySelector("#compoundForm");
const nameInput = document.querySelector("#compoundName");
const smilesInput = document.querySelector("#smilesInput");
const table = document.querySelector("#compoundTable");
const libraryCount = document.querySelector("#libraryCount");
const canvas = document.querySelector("#moleculeCanvas");
const ctx = canvas.getContext("2d");

function tokenizeSmiles(smiles) {
  return smiles.match(/Cl|Br|[A-Z][a-z]?|[cnosp]|\[[^\]]+\]/g) || [];
}

function countAtoms(smiles) {
  const counts = {};
  for (const token of tokenizeSmiles(smiles)) {
    let atom = token;

    if (token.startsWith("[")) {
      const match = token.match(/[A-Z][a-z]?|[cnosp]/);
      if (!match) continue;
      atom = match[0];
    }

    atom = atom.length === 1 ? atom.toUpperCase() : atom[0].toUpperCase() + atom.slice(1);
    if (!ATOMIC_WEIGHTS[atom]) continue;
    counts[atom] = (counts[atom] || 0) + 1;
  }
  return counts;
}

function estimateProperties(smiles) {
  const atoms = countAtoms(smiles);
  const carbons = atoms.C || 0;
  const nitrogens = atoms.N || 0;
  const oxygens = atoms.O || 0;
  const sulfurs = atoms.S || 0;
  const halogens = (atoms.F || 0) + (atoms.Cl || 0) + (atoms.Br || 0) + (atoms.I || 0);
  const hetero = nitrogens + oxygens + sulfurs + (atoms.P || 0);
  const ringHints = new Set(smiles.match(/\d/g) || []).size;
  const branches = (smiles.match(/\(/g) || []).length;
  const doubleBonds = (smiles.match(/=/g) || []).length;
  const aromatic = (smiles.match(/[cnosp]/g) || []).length;

  const heavyMw = Object.entries(atoms).reduce(
    (sum, [atom, count]) => sum + ATOMIC_WEIGHTS[atom] * count,
    0,
  );
  const hydrogenEstimate = Math.max(0, carbons * 2 + 2 - hetero - halogens - ringHints * 2 - doubleBonds * 2);
  const molecularWeight = heavyMw + hydrogenEstimate * ATOMIC_WEIGHTS.H;
  const hbd = Math.min(oxygens + nitrogens, (smiles.match(/[NO][H\]]?|[no]H/g) || []).length + oxygens);
  const hba = oxygens + nitrogens + Math.floor(sulfurs * 0.5);
  const logp = carbons * 0.54 + halogens * 0.65 + aromatic * 0.12 - hetero * 1.05 - branches * 0.08;
  const tpsa = oxygens * 17 + nitrogens * 12 + sulfurs * 25 + (atoms.P || 0) * 38;
  const violations = [
    molecularWeight > 500,
    logp > 5,
    hbd > 5,
    hba > 10,
  ].filter(Boolean).length;

  return {
    engine: "Local",
    formula: "--",
    exactMass: molecularWeight,
    molarRefractivity: "--",
    atoms,
    molecularWeight,
    logp,
    hbd,
    hba,
    tpsa,
    rotatableBonds: branches,
    heavyAtoms: Object.values(atoms).reduce((sum, count) => sum + count, 0),
    ringCount: ringHints,
    aromaticRings: ringHints && aromatic ? 1 : 0,
    fractionCsp3: "--",
    formalCharge: 0,
    violations,
    lipinski: violations === 0 ? "Pass" : violations === 1 ? "Caution" : "Fail",
  };
}

async function getProperties(smiles) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ smiles }),
    });

    if (!response.ok) {
      throw new Error("Backend request failed");
    }

    const data = await response.json();
    if (!data.ok) {
      throw new Error(data.error || "Invalid molecule");
    }

    return {
      engine: "RDKit",
      formula: data.formula,
      molecularWeight: data.molecular_weight,
      exactMass: data.exact_mass,
      logp: data.logp,
      molarRefractivity: data.molar_refractivity,
      hbd: data.hbd,
      hba: data.hba,
      tpsa: data.tpsa,
      rotatableBonds: data.rotatable_bonds,
      heavyAtoms: data.heavy_atoms,
      ringCount: data.ring_count,
      aromaticRings: data.aromatic_rings,
      fractionCsp3: data.fraction_csp3,
      formalCharge: data.formal_charge,
      lipinski: data.lipinski,
      violations: data.lipinski === "Pass" ? 0 : data.lipinski === "Caution" ? 1 : 2,
    };
  } catch (error) {
    const fallback = estimateProperties(smiles);
    fallback.engine = "Local";
    return fallback;
  }
}

function drawMolecule(smiles) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#f7fbf9";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const atoms = tokenizeSmiles(smiles)
    .map((token) => token.replace(/[\[\]]/g, ""))
    .filter((token) => /Cl|Br|[A-Z][a-z]?|[cnosp]/.test(token))
    .slice(0, 18);

  if (!atoms.length) {
    ctx.fillStyle = "#60706a";
    ctx.font = "16px Segoe UI";
    ctx.fillText("Enter a SMILES string", 138, 134);
    return;
  }

  const centerY = canvas.height / 2;
  const startX = Math.max(42, canvas.width / 2 - atoms.length * 18);
  const spacing = Math.min(42, 330 / Math.max(1, atoms.length - 1));

  atoms.forEach((atom, index) => {
    const x = startX + index * spacing;
    const y = centerY + Math.sin(index * 1.35) * 42;

    if (index > 0) {
      const previousX = startX + (index - 1) * spacing;
      const previousY = centerY + Math.sin((index - 1) * 1.35) * 42;
      ctx.strokeStyle = "#8aa39d";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(previousX, previousY);
      ctx.lineTo(x, y);
      ctx.stroke();
    }

    const normalized = atom.length === 1 ? atom.toUpperCase() : atom;
    const color = normalized.startsWith("O")
      ? "#dc2626"
      : normalized.startsWith("N")
        ? "#2563eb"
        : normalized.startsWith("S")
          ? "#ca8a04"
          : normalized === "Cl" || normalized === "Br" || normalized === "F"
            ? "#16a34a"
            : "#243b35";

    ctx.fillStyle = "#ffffff";
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(x, y, 17, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = color;
    ctx.font = "700 13px Segoe UI";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(normalized[0].toUpperCase() + normalized.slice(1), x, y);
  });
}

function updateMetrics(result) {
  document.querySelector("#engineValue").textContent = result.engine;
  document.querySelector("#mwValue").textContent = result.molecularWeight.toFixed(1);
  document.querySelector("#formulaValue").textContent = result.formula ?? "--";
  document.querySelector("#exactMassValue").textContent = Number(result.exactMass).toFixed(2);
  document.querySelector("#logpValue").textContent = result.logp.toFixed(2);
  document.querySelector("#mrValue").textContent =
    typeof result.molarRefractivity === "number" ? result.molarRefractivity.toFixed(1) : "--";
  document.querySelector("#hbdValue").textContent = result.hbd;
  document.querySelector("#hbaValue").textContent = result.hba;
  document.querySelector("#tpsaValue").textContent = result.tpsa.toFixed(0);
  document.querySelector("#rotatableValue").textContent = result.rotatableBonds ?? "--";
  document.querySelector("#heavyAtomsValue").textContent = result.heavyAtoms ?? "--";
  document.querySelector("#ringsValue").textContent = result.ringCount ?? "--";
  document.querySelector("#aromaticRingsValue").textContent = result.aromaticRings ?? "--";
  document.querySelector("#fractionCsp3Value").textContent = result.fractionCsp3 ?? "--";
  document.querySelector("#chargeValue").textContent = result.formalCharge ?? "--";
  document.querySelector("#lipinskiValue").textContent = result.lipinski;
}

function renderTable() {
  table.innerHTML = library
    .map((compound) => {
      const badgeClass =
        compound.lipinski === "Pass" ? "good" : compound.lipinski === "Caution" ? "warn" : "bad";
      return `
        <tr>
          <td>${compound.name}</td>
          <td class="smiles-cell">${compound.smiles}</td>
          <td>${compound.formula ?? "--"}</td>
          <td>${compound.molecularWeight.toFixed(1)}</td>
          <td>${compound.logp.toFixed(2)}</td>
          <td>${compound.hbd}</td>
          <td>${compound.hba}</td>
          <td>${compound.tpsa.toFixed(0)}</td>
          <td>${compound.rotatableBonds ?? "--"}</td>
          <td><span class="badge ${badgeClass}">${compound.lipinski}</span></td>
        </tr>
      `;
    })
    .join("");
  libraryCount.textContent = `${library.length} compound${library.length === 1 ? "" : "s"}`;
}

async function analyzeCompound(name, smiles) {
  const result = await getProperties(smiles);
  const compound = {
    name: name || `Compound ${library.length + 1}`,
    smiles,
    ...result,
  };
  library = [compound, ...library];
  updateMetrics(result);
  drawMolecule(smiles);
  renderTable();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const smiles = smilesInput.value.trim();
  if (!smiles) return;
  await analyzeCompound(nameInput.value.trim(), smiles);
});

document.querySelector("#loadExamples").addEventListener("click", async () => {
  library = [];
  for (const compound of examples) {
    const result = await getProperties(compound.smiles);
    library.push({ ...compound, ...result });
  }
  nameInput.value = examples[0].name;
  smilesInput.value = examples[0].smiles;
  updateMetrics(library[0]);
  drawMolecule(examples[0].smiles);
  renderTable();
});

document.querySelector("#exportCsv").addEventListener("click", () => {
  const rows = [
    ["Name", "SMILES", "MW", "LogP", "HBD", "HBA", "TPSA", "Lipinski"],
    ...library.map((compound) => [
      compound.name,
      compound.smiles,
      compound.formula ?? "",
      compound.molecularWeight.toFixed(1),
      compound.logp.toFixed(2),
      compound.hbd,
      compound.hba,
      compound.tpsa.toFixed(0),
      compound.rotatableBonds ?? "",
      compound.lipinski,
    ]),
  ];
  const csv = rows.map((row) => row.map((cell) => `"${String(cell).replaceAll('"', '""')}"`).join(",")).join("\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "insilicolab-compounds.csv";
  link.click();
  URL.revokeObjectURL(url);
});

drawMolecule("");
