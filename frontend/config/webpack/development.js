let webpack = require('webpack')

import config from '../'
import webpackConfig from './_base'

export default {
  ...webpackConfig,
  devtool: 'cheap-module-eval-source-map',
  entry: {
    ...webpackConfig.entry,
    bundle: [
      `webpack-dev-server/client?http://${config.get('webpack_host')}:${config.get('webpack_port')}`,
      'webpack/hot/only-dev-server',
      'react-hot-loader/patch',
      ...webpackConfig.entry.bundle
    ]
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    ...webpackConfig.plugins
  ]
}
