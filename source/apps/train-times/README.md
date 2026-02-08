# Next Trains PWA

A Progressive Web App for checking UK rail departure times using the Huxley2 API.

## Features

- 🚆 Check two journeys simultaneously
- 💾 Remembers your last searches (localStorage)
- 📱 Install as an app on your phone
- ⚡ Fast, responsive design
- 🌙 Dark theme optimized for mobile
- 📶 Offline support with service worker

## Quick Start

### 1. Create Icon Images

You need to convert the `icon.svg` to PNG images. You can use an online converter like [CloudConvert](https://cloudconvert.com/svg-to-png) or ImageMagick:

```bash
# Using ImageMagick (if installed)
convert -background none icon.svg -resize 192x192 icon-192.png
convert -background none icon.svg -resize 512x512 icon-512.png
```

Or use any online SVG to PNG converter to create:
- `icon-192.png` (192x192 pixels)
- `icon-512.png` (512x512 pixels)

### 2. Deploy to GitHub Pages

1. Create a new GitHub repository
2. Upload these files:
   - `index.html`
   - `manifest.json`
   - `service-worker.js`
   - `icon-192.png`
   - `icon-512.png`

3. Enable GitHub Pages:
   - Go to repository Settings → Pages
   - Source: Deploy from branch
   - Branch: `main` (or `master`), folder: `/root`
   - Click Save

4. Your app will be available at: `https://yourusername.github.io/repositoryname`

### Alternative: Deploy to Netlify

1. Drag and drop all files to [Netlify Drop](https://app.netlify.com/drop)
2. Your app is instantly live!

## Usage

### Station Codes (CRS)

UK stations use 3-letter CRS codes. Common examples:
- **HSL** - Haslemere
- **WAT** - London Waterloo
- **VIC** - London Victoria
- **CLJ** - Clapham Junction
- **GLD** - Guildford
- **WOK** - Woking

Find station codes at: https://www.nationalrail.co.uk/stations/

### Using the App

1. Enter departure station code (3 letters)
2. Enter destination station code (3 letters)
3. Click "Get Next Trains"
4. View the next 5 departures with:
   - Scheduled departure time
   - Platform number
   - Operator
   - Status (On time / Delayed / Cancelled)

### Installing on Android

1. Open the app in Chrome
2. Tap the menu (⋮) → "Add to Home screen"
3. The app will appear on your home screen like a native app
4. Opens in fullscreen without browser UI

## How It Works

- **Huxley2 API**: Uses the public Huxley2 instance (REST wrapper for National Rail Darwin API)
- **localStorage**: Saves your last searched routes automatically
- **Service Worker**: Caches the app for offline use (API calls still need internet)
- **PWA**: Meets Progressive Web App standards for installation

## API Information

This app uses the public Huxley2 API endpoint:
```
https://huxley2.azurewebsites.net/departures/{from}/to/{to}
```

No API key required for the public instance. If you experience rate limiting, you can:
1. Host your own Huxley2 instance: https://github.com/jpsingleton/Huxley2
2. Get a National Rail Darwin API key and update the Huxley2 URL

## Customization

### Colors

Edit the CSS variables in `index.html`:
```css
:root {
    --bg-primary: #0f0f1e;
    --bg-secondary: #1a1a2e;
    --bg-card: #16213e;
    --accent-primary: #e94560;
    /* etc... */
}
```

### Default Stations

You can pre-fill stations by modifying the placeholder text or default values in the input fields.

### Number of Results

Change the slice value in the JavaScript:
```javascript
const services = data.trainServices.slice(0, 5); // Change 5 to desired number
```

## Browser Support

- Chrome/Edge (Android): Full PWA support
- Safari (iOS): Basic PWA support (can add to home screen)
- Firefox: Works but limited PWA features

## Troubleshooting

**No trains found:**
- Check station codes are correct (3 letters)
- Ensure there are direct trains between stations
- Try different times of day

**App not installing:**
- Use Chrome on Android for best experience
- Ensure app is served over HTTPS (automatic on GitHub Pages/Netlify)

**API errors:**
- Public Huxley2 instance may have rate limits
- Check https://huxley2.azurewebsites.net/all is accessible

## License

MIT - Feel free to modify and use as you wish!

## Credits

- [Huxley2](https://github.com/jpsingleton/Huxley2) by JP Singleton
- National Rail Darwin API
