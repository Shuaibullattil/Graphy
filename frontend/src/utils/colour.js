export function generateOrderedShades(labels) {
  const baseHue = 275;
  const baseSaturation = 45;
  const saturationRange = [40, 50];
  const lightnessRange = [60, 80];

  const generated = new Set();
  const shades = [];

  while (shades.length < labels.length) {
    const saturation = Math.floor(Math.random() * (saturationRange[1] - saturationRange[0] + 1)) + saturationRange[0];
    const lightness = Math.floor(Math.random() * (lightnessRange[1] - lightnessRange[0] + 1)) + lightnessRange[0];
    const color = `hsl(${baseHue}, ${saturation}%, ${lightness}%)`;
    
    if (!generated.has(color)) {
      generated.add(color);
      shades.push({ color, lightness });
    }
  }

  // Sort by lightness descending
  shades.sort((a, b) => b.lightness - a.lightness);
  return shades.map(shade => shade.color);
}
