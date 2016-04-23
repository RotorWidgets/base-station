require('babel-register')

var chalk = require('chalk')
var config = require('./config').default

var host = config.get('webpack_host')
var port = config.get('webpack_port')

// New stuff example from webpack-dev-server
var WebpackDevServer = require('webpack-dev-server')
var webpack = require('webpack')
// import gzipStatic from 'connect-gzip-static'

var webpackConfig = require('./webpack.config')
var compiler = webpack(webpackConfig)

var isDevelopment = config.get('env').NODE_ENV === 'development'
var staticDir = config.get(isDevelopment ? 'dir_src' : 'dir_dist')

var server = new WebpackDevServer(compiler, {
  // webpack-dev-server options

  contentBase: staticDir,

  hot: true,
  // Enable special support for Hot Module Replacement
  // Page is no longer updated, but a 'webpackHotUpdate' message is send to the content
  // Use 'webpack/hot/dev-server' as additional module in your entry point
  // Note: this does _not_ add the `HotModuleReplacementPlugin` like the CLI option does.

  // Set this as true if you want to access dev server from arbitrary url.
  // This is handy if you are using a html5 router.
  // historyApiFallback: false,

  // Set this if you want webpack-dev-server to delegate a single path to an arbitrary server.
  // Use '*' to proxy all paths to the specified server.
  // This is useful if you want to get rid of 'http://localhost:8080/' in script[src],
  // and has many other use cases (see https://github.com/webpack/webpack-dev-server/pull/127 ).
  proxy: {
    '/*': {
      target: config.get('proxy'),
      secure: false
    }
  },

  // webpack-dev-middleware options
  quiet: false,
  noInfo: false,
  // lazy: true,
  filename: 'bundle.js',
  // watchOptions: {
  //   aggregateTimeout: 300,
  //   poll: 1000
  // },

  // publicPath: webpackConfig.output.publicPath,
  // headers: {
  // },
  stats: {
    colors: true,
    hash: true,
    timings: true,
    chunks: true,
    chunkModules: false,
    modules: true
  }
})

server.listen(port, host, () => {
  console.log(`⚡  Server running at ${chalk.white(`${host}:${port}`)}`)
})
