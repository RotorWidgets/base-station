import path from 'path'
import webpack from 'webpack'

import config from '../'

let path_project = config.get('path_project')

export default {
  target: 'web',
  devtool: '#source-map',
  entry: {
    bundle: [path.join(config.get('dir_src'), 'index.jsx')]
  },
  output: {
    path: path.join(config.get('dir_dist'), config.get('globals').__BASE__),
    pathInfo: true,
    publicPath: `/${config.get('globals').__BASE__}`,
    filename: 'bundle.js'
  },
  module: {
    preLoaders: [],
    loaders: [
      {
        test: /\.jsx?$/,
        loader: 'babel',
        exclude: ['node_modules'],
        include: `${config.get('dir_src')}`
      },
      {
        test: /\.json$/,
        loader: 'json'
      }
    ],
    noParse: [/\.min\.js$/]
  },
  resolve: {
    extensions: ['', '.js', '.jsx'],
    modulesDirectories: ['web_modules', 'node_modules'],
    alias: {
      react: path.resolve(path.join(path_project, 'node_modules', 'react')),
      components: path.resolve(path.join(config.get('path_project'), 'src', 'components')),
      containers: path.resolve(path.join(config.get('path_project'), 'src', 'containers'))
    }
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': config.get('globals')['process.env'],
      __DEV__: JSON.stringify(config.get('globals').__DEV__),
      __PROD__: JSON.stringify(config.get('globals').__PROD__),
      __DEBUG__: JSON.stringify(config.get('globals').__DEBUG__),
      __BASE__: JSON.stringify(config.get('globals').__BASE__)
    })
  ]
}
