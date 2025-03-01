module.exports = {
    content: ['./**/*.html', './**/*.js'], // This will search for HTML and JS files in your Django project
    css: ['./static/bootstrap.min.css'], // Replace with the path to your Bootstrap CSS file
    output: './static/css/', // The output directory for the cleaned CSS file
    defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
    safelist: [], // Add any classes or patterns that you want to keep even if they're not found in your HTML/JS files
  };