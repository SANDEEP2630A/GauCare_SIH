export const cowData = {
  "COW-027": [
    { date: "2026-08-16", conductivity: 4.2, temperature: 38.5, spectral_dev: "Normal", risk: 12, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-17", conductivity: 4.4, temperature: 38.6, spectral_dev: "Normal", risk: 18, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-18", conductivity: 5.1, temperature: 38.7, spectral_dev: "Normal", risk: 28, factors: { conductivity: "Medium", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-19", conductivity: 5.8, temperature: 38.9, spectral_dev: "Mild Deviation", risk: 42, factors: { conductivity: "Medium", spectral: "Medium", temperature: "Low", trend: "Medium" } },
    { date: "2026-08-20", conductivity: 6.2, temperature: 39.1, spectral_dev: "Deviation", risk: 58, factors: { conductivity: "Medium", spectral: "Medium", temperature: "Medium", trend: "Medium" } },
    { date: "2026-08-21", conductivity: 7.1, temperature: 39.4, spectral_dev: "Significant", risk: 76, factors: { conductivity: "High", spectral: "High", temperature: "Medium", trend: "High" } },
    { date: "2026-08-22", conductivity: 7.8, temperature: 39.6, spectral_dev: "Significant", risk: 84, factors: { conductivity: "High", spectral: "High", temperature: "High", trend: "High" } },
  ],
  "COW-103": [
    { date: "2026-08-16", conductivity: 3.9, temperature: 38.4, spectral_dev: "Normal", risk: 8, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-17", conductivity: 4.0, temperature: 38.4, spectral_dev: "Normal", risk: 10, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-18", conductivity: 4.1, temperature: 38.5, spectral_dev: "Normal", risk: 11, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-19", conductivity: 4.0, temperature: 38.4, spectral_dev: "Normal", risk: 9, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-20", conductivity: 4.2, temperature: 38.5, spectral_dev: "Normal", risk: 12, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-21", conductivity: 4.1, temperature: 38.4, spectral_dev: "Normal", risk: 10, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-22", conductivity: 4.0, temperature: 38.3, spectral_dev: "Normal", risk: 8, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
  ],
  "COW-054": [
    { date: "2026-08-16", conductivity: 5.0, temperature: 38.7, spectral_dev: "Mild Deviation", risk: 32, factors: { conductivity: "Medium", spectral: "Medium", temperature: "Low", trend: "Low" } },
    { date: "2026-08-17", conductivity: 5.6, temperature: 38.9, spectral_dev: "Deviation", risk: 48, factors: { conductivity: "Medium", spectral: "Medium", temperature: "Medium", trend: "Medium" } },
    { date: "2026-08-18", conductivity: 6.5, temperature: 39.3, spectral_dev: "Significant", risk: 68, factors: { conductivity: "High", spectral: "High", temperature: "Medium", trend: "High" } },
    { date: "2026-08-19", conductivity: 7.2, temperature: 39.6, spectral_dev: "Significant", risk: 78, factors: { conductivity: "High", spectral: "High", temperature: "High", trend: "High" } },
    { date: "2026-08-20", conductivity: 7.8, temperature: 39.8, spectral_dev: "Critical", risk: 88, factors: { conductivity: "High", spectral: "High", temperature: "High", trend: "High" } },
    { date: "2026-08-21", conductivity: 8.1, temperature: 39.9, spectral_dev: "Critical", risk: 92, factors: { conductivity: "High", spectral: "High", temperature: "High", trend: "High" } },
    { date: "2026-08-22", conductivity: 8.0, temperature: 39.8, spectral_dev: "Critical", risk: 90, factors: { conductivity: "High", spectral: "High", temperature: "High", trend: "High" } },
  ],
  "COW-089": [
    { date: "2026-08-16", conductivity: 4.8, temperature: 38.6, spectral_dev: "Normal", risk: 22, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-17", conductivity: 5.3, temperature: 38.7, spectral_dev: "Mild Deviation", risk: 35, factors: { conductivity: "Medium", spectral: "Medium", temperature: "Low", trend: "Medium" } },
    { date: "2026-08-18", conductivity: 5.5, temperature: 38.7, spectral_dev: "Mild Deviation", risk: 38, factors: { conductivity: "Medium", spectral: "Medium", temperature: "Low", trend: "Medium" } },
    { date: "2026-08-19", conductivity: 5.4, temperature: 38.6, spectral_dev: "Normal", risk: 32, factors: { conductivity: "Medium", spectral: "Low", temperature: "Low", trend: "Medium" } },
    { date: "2026-08-20", conductivity: 5.2, temperature: 38.5, spectral_dev: "Normal", risk: 26, factors: { conductivity: "Medium", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-21", conductivity: 5.0, temperature: 38.5, spectral_dev: "Normal", risk: 22, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
    { date: "2026-08-22", conductivity: 4.9, temperature: 38.4, spectral_dev: "Normal", risk: 18, factors: { conductivity: "Low", spectral: "Low", temperature: "Low", trend: "Low" } },
  ],
};

export function getRiskClass(score) {
  if (score < 30) return "low";
  if (score < 60) return "moderate";
  return "high";
}

export function getRiskLabel(score) {
  if (score < 30) return "Low Risk";
  if (score < 60) return "Moderate Risk";
  return "High Risk";
}

export function getRecommendation(score) {
  if (score < 30) return "Risk is low. Continue routine monitoring. No immediate action required.";
  if (score < 60) return "Elevated risk detected. Recommend close observation and possible veterinary consultation within 48 hours.";
  return "High mastitis risk detected. Recommend veterinary examination within 24\u201348 hours. Isolate cow pending assessment.";
}

export const factorMeta = [
  { key: "conductivity", label: "Conductivity Deviation", isUp: true, barMax: 90 },
  { key: "spectral", label: "Spectral Deviation", isUp: true, barMax: 85 },
  { key: "temperature", label: "Temperature Anomaly", isUp: false, barMax: 60 },
  { key: "trend", label: "Recent Risk Trend", isUp: true, barMax: 80 },
];
