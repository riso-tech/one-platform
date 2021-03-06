////////////////////////////////
// Setup
////////////////////////////////

// Gulp and package
const { src, dest, parallel, series, watch } = require('gulp')
const pjson = require('./package.json')

// Plugins
const autoprefixer = require('autoprefixer')
const browserSync = require('browser-sync').create()
const concat = require('gulp-concat')
const cssnano = require ('cssnano')
const imagemin = require('gulp-imagemin')
const pixrem = require('pixrem')
const plumber = require('gulp-plumber')
const postcss = require('gulp-postcss')
const reload = browserSync.reload
const rename = require('gulp-rename')
const sass = require('gulp-sass')(require('sass'))
const spawn = require('child_process').spawn
const uglify = require('gulp-uglify-es').default

// Relative paths function
function pathsConfig(appName) {
  this.app = `./${pjson.name}`
  const vendorsRoot = 'node_modules'

  return {
    bootstrapSass: `${vendorsRoot}/bootstrap/scss`,
    vendorsJs: [
      `${vendorsRoot}/dropify/dist/js/dropify.js`,
      `${vendorsRoot}/jquery-mask-plugin/dist/jquery.mask.js`,
      `${vendorsRoot}/jquery.json-viewer/json-viewer/jquery.json-viewer.js`,
    ],
    vendorsStyles: [
      `${vendorsRoot}/dropify/dist/css/dropify.css`,
      `${vendorsRoot}/jquery.json-viewer/json-viewer/jquery.json-viewer.css`,
    ],
    vendorsFonts: [
      `${vendorsRoot}/dropify/dist/fonts/*.*`,
    ],
    vendorsImages: [
      `${vendorsRoot}/dropify/src/images/*`,
    ],
    app: this.app,
    templates: `${this.app}/templates`,
    css: `${this.app}/static/css`,
    sass: `${this.app}/static/sass`,
    fonts: `${this.app}/static/fonts`,
    images: `${this.app}/static/images`,
    js: `${this.app}/static/js`,
  }
}

var paths = pathsConfig()

////////////////////////////////
// Tasks
////////////////////////////////

// Styles autoprefixing and minification
function styles() {
  var processCss = [
      autoprefixer(), // adds vendor prefixes
      pixrem(),       // add fallbacks for rem units
  ]

  var minifyCss = [
      cssnano({ preset: 'default' })   // minify result
  ]

  return src(`${paths.sass}/project.scss`)
    .pipe(sass({
      includePaths: [
        // paths.bootstrapSass,
        paths.sass
      ]
    }).on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(dest(paths.css))
}

// Vendor Styles minification
function vendorStyles() {
  var processCss = [
      autoprefixer(), // adds vendor prefixes
      pixrem(),       // add fallbacks for rem units
  ]

  var minifyCss = [
      cssnano({ preset: 'default' })   // minify result
  ]

  return src(paths.vendorsStyles)
    .pipe(concat('vendors.css'))
    .pipe(dest(paths.css))
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(dest(paths.css))
}

// Javascript minification
function scripts() {
  return src(`${paths.js}/project.js`)
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js))
}

// Vendor Javascript minification
function vendorScripts() {
  return src(paths.vendorsJs)
    .pipe(concat('vendors.js'))
    .pipe(dest(paths.js))
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js))
}

// Vendor Assets Collector
// Fonts
function vendorFonts() {
  return src(paths.vendorsFonts)
    .pipe(dest(paths.fonts))
}
// Images
function vendorImages() {
  return src(paths.vendorsImages, {"allowEmpty": true})
    .pipe(dest(paths.images))
}


// Image compression
function imgCompression() {
  return src(`${paths.images}/*`)
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(dest(paths.images))
}// Run django server

function asyncRunServer() {
  var cmd = spawn('gunicorn', [
      'config.asgi', '-k', 'uvicorn.workers.UvicornWorker', '--reload'
      ], {stdio: 'inherit'}
  )
  cmd.on('close', function(code) {
    console.log('gunicorn exited with code ' + code)
  })
}

// Browser sync server for live reload
function initBrowserSync() {
  browserSync.init(
    [
      `${paths.css}/*.css`,
      `${paths.js}/*.js`,
      `${paths.templates}/*.html`
    ], {
      // https://www.browsersync.io/docs/options/#option-open
      // Disable as it doesn't work from inside a container
      open: false,
      // https://www.browsersync.io/docs/options/#option-proxy
      proxy:  {
        // target: 'django:8000', // Using Docker
        target: 'localhost:8000', // Using Django
        proxyReq: [
          function(proxyReq, req) {
            // Assign proxy "host" header same as current request at Browsersync server
            proxyReq.setHeader('Host', req.headers.host)
          }
        ]
      }
    }
  )
}

// Watch
function watchPaths() {
  watch(`${paths.sass}/*.scss`, styles)
  watch(`${paths.templates}/**/*.html`).on("change", reload)
  watch([`${paths.js}/*.js`, `!${paths.js}/*.min.js`], scripts).on("change", reload)
}

// Generate all assets
const generateAssets = parallel(
  styles,
  vendorStyles,
  scripts,
  vendorScripts,
  vendorFonts,
  vendorImages,
  imgCompression
)

// Set up dev environment
const dev = parallel(
  initBrowserSync,
  watchPaths
)

exports.default = series(generateAssets, dev)
exports["generate-assets"] = generateAssets
exports["dev"] = dev
