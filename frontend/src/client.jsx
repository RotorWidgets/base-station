import {render} from 'react-dom'
import React from 'react'
import { AppContainer } from 'react-hot-loader'
import Router from './containers/Router'

render(
  <AppContainer component={Router}/>,
  document.getElementById('root')
)

if (module.hot) {
  module.hot.accept('./containers/Router', () => {
    render(
      <AppContainer
        component={require('./containers/Router').default}
      />,
      document.getElementById('root')
    )
  })
}
