import {render} from 'react-dom'
import React from 'react'

import { AppContainer } from 'react-hot-loader'
import Root from 'containers/Root'

render(
  <AppContainer
    component={Root}
  />,
  document.getElementById('root')
)

if (module.hot) {
  module.hot.accept('./containers/Root', () => {
    render(
      <AppContainer
        component={require('./containers/Root').default}
      />,
      document.getElementById('root')
    )
  })
}
