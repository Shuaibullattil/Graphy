
// for VIOLET SHADES
// export function generateOrderedShades(labels) {
//   const baseHue = 275;
//   const baseSaturation = 45;
//   const saturationRange = [40, 50];
//   const lightnessRange = [60, 80];

//   const generated = new Set();
//   const shades = [];

//   while (shades.length < labels.length) {
//     const saturation = Math.floor(Math.random() * (saturationRange[1] - saturationRange[0] + 1)) + saturationRange[0];
//     const lightness = Math.floor(Math.random() * (lightnessRange[1] - lightnessRange[0] + 1)) + lightnessRange[0];
//     const color = `hsl(${baseHue}, ${saturation}%, ${lightness}%)`;
    
//     if (!generated.has(color)) {
//       generated.add(color);
//       shades.push({ color, lightness });
//     }
//   }

//   // Sort by lightness descending
//   shades.sort((a, b) => b.lightness - a.lightness);
//   return shades.map(shade => shade.color);
// }


// for unique shades
// export function generateOrderedShades(labels) {
//   const total = labels.length;
//   const saturation = 65; // Fixed saturation for vibrancy
//   const lightness = 60;  // Fixed lightness for balance
//   const usedHues = new Set();
//   const colors = [];

//   for (let i = 0; i < total; i++) {
//     let hue;

//     // Generate unique hues spaced around the 360° hue circle
//     if (total <= 360) {
//       hue = Math.floor((360 / total) * i);
//     } else {
//       // More labels than hues, use random hue ensuring uniqueness
//       do {
//         hue = Math.floor(Math.random() * 360);
//       } while (usedHues.has(hue));
//     }

//     usedHues.add(hue);
//     colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
//   }

//   return colors;
// }


/// for unique shades with a randomly chosen base color
export function generateOrderedShades(labels) {
  const total = labels.length;
  const saturationRange = [50, 90];
  const lightnessRange = [40, 80];
  const usedCombinations = new Set();
  const colors = [];

  // Random base hue
  const baseHue = Math.floor(Math.random() * 360);

  while (colors.length < total) {
    const saturation = Math.floor(Math.random() * (saturationRange[1] - saturationRange[0] + 1)) + saturationRange[0];
    const lightness = Math.floor(Math.random() * (lightnessRange[1] - lightnessRange[0] + 1)) + lightnessRange[0];
    const key = `${saturation}-${lightness}`;

    // Ensure no duplicate saturation-lightness pair
    if (!usedCombinations.has(key)) {
      usedCombinations.add(key);
      const color = `hsl(${baseHue}, ${saturation}%, ${lightness}%)`;
      colors.push(color);
    }
  }

  return colors;
}

