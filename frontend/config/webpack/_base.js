import path from 'path'
import webpack from 'webpack'

import config from '../'

let path_project = config.get('path_project')
let src_dir = path.join(config.get('path_project'), 'src')

export default {
  target: 'web',
  devtool: 'source-map',
  entry: {
    bundle: [path.join(config.get('dir_src'), 'client.jsx')]
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
        include: `${config.get('dir_src')}`,
        query: {
          // This can't be loaded through .babelrc for some reason.
          plugins: [`${path_project}/plugins/babelRelayPlugin`]
        }
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
      components: path.resolve(path.join(src_dir, 'components')),
      containers: path.resolve(path.join(src_dir, 'containers')),
      mutations: path.resolve(path.join(src_dir, 'mutations')),
      queries: path.resolve(path.join(src_dir, 'queries'))
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
