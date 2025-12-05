# Holi-Daze Progress Bar 🎄

A festive, real-time progress bar for the $HOLI memecoin on the Base chain, tracking the journey to a 30K Market Cap.

## Features
- **Real-time Data**: Fetches live market cap data from the DexScreener API.
- **Base Chain Optimized**: Automatically prioritizes Base chain pairs.
- **Festive UI**: Christmas-themed animations, gradients, and styling.
- **Responsive**: Looks great on desktop and mobile.

## Setup
1. Simply open `index.html` in any web browser.
2. The progress bar will load the current market cap and update every 30 seconds.

## Configuration
You can modify the target market cap or contract address in `index.html`:
```javascript
const CONTRACT_ADDRESS = '0xD0Dce4A1aC8D6195a9628800cE518e278808d11a';
const TARGET_MC = 30000;
```

## Hosting
To share this with your community, you can enable **GitHub Pages**:
1. Go to the repository Settings.
2. Scroll down to "Pages".
3. Select `main` branch as the source.
4. Your site will be live at `https://<your-username>.github.io/Holi-counter/`.