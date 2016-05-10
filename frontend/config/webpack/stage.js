// Stage configuration is for configuring a production build without compressing or cleaning any bundled files
// Usuful to make test the production build and any errors that may come up.
import webpack from 'webpack'
import BundleTracker from 'webpack-bundle-tracker'
// FIX: clean-webpack-plugin deletes directory which causes issues, find an alternative
// import CleanWebpackPlugin from 'clean-webpack-plugin'

import config from '../'
import webpackConfig from './_base'

const LIBS_BUNDLE = 'libs'

export default {
  ...webpackConfig,
  entry: {
    ...webpackConfig.entry,
    [LIBS_BUNDLE]: config.get('dependencies')
  },
  output: {
    ...webpackConfig.output,
    filename: '[name].[hash].js',
    chunkFilename: '[id].js'
  },
  plugins: [
    ...webpackConfig.plugins,
    new webpack.optimize.CommonsChunkPlugin(LIBS_BUNDLE, `${LIBS_BUNDLE}.[hash].js`),
    new BundleTracker({
      filename: './webpack-stats.json'
    })
    // new CleanWebpackPlugin(['dist'], {
    //   root: config.get('path_project')
    // })
  ]
}
