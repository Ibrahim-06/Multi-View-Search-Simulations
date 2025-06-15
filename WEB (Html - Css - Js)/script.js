let globalArr = [];

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function updateArray() {
  const val = document.getElementById("arrayInput").value;
  globalArr = val
    .split(",")
    .map((x) => parseInt(x))
    .filter((x) => !isNaN(x));
  renderCircleArray(globalArr);
}

function renderCircleArray(
  arr,
  highlightIndex = -1,
  foundIndex = -1,
  notfound = false
) {
  const container = document.getElementById("arrayDisplay");
  container.innerHTML = "";
  const radius = 150;
  const centerX = 200;
  const centerY = 200;

  arr.forEach((val, idx) => {
    const angle = ((2 * Math.PI) / arr.length) * idx;
    const x = centerX + radius * Math.cos(angle) - 30;
    const y = centerY + radius * Math.sin(angle) - 30;

    const elem = document.createElement("div");
    elem.className = "array-element";
    elem.style.left = `${x}px`;
    elem.style.top = `${y}px`;
    elem.textContent = val;

    if (idx === highlightIndex) elem.classList.add("highlight");
    if (idx === foundIndex) elem.classList.add("found");
    if (notfound) elem.classList.add("notfound");

    container.appendChild(elem);
  });
}

async function bruteForceSearch() {
  const output = document.getElementById("output");
  const target = parseInt(document.getElementById("target").value);
  output.textContent = "";

  for (let i = 0; i < globalArr.length; i++) {
    renderCircleArray(globalArr, i);
    output.textContent = `🚀 Scanning position ${i}`;
    await sleep(700);
    if (globalArr[i] === target) {
      renderCircleArray(globalArr, -1, i);
      output.textContent = `✅ Found ${target} at position ${i}`;
      return;
    }
  }
  renderCircleArray(globalArr, -1, -1, true);
  output.textContent = `❌ ${target} not found`;
}

async function binarySearch() {
  const output = document.getElementById("output");
  let sorted = [...globalArr].sort((a, b) => a - b);
  renderCircleArray(sorted);
  const target = parseInt(document.getElementById("target").value);
  let low = 0,
    high = sorted.length - 1;

  while (low <= high) {
    let mid = Math.floor((low + high) / 2);
    renderCircleArray(sorted, mid);
    output.textContent = `🔍 Checking position ${mid}`;
    await sleep(800);

    if (sorted[mid] === target) {
      renderCircleArray(sorted, -1, mid);
      output.textContent = `✅ Found ${target} at position ${mid}`;
      return;
    } else if (sorted[mid] < target) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  renderCircleArray(sorted, -1, -1, true);
  output.textContent = `❌ ${target} not found`;
}
