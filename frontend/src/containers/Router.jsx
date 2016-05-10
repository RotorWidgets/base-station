import React, { Component } from 'react'

// routing requirements
import { applyRouterMiddleware, Router, useRouterHistory } from 'react-router'
import useRelay from 'react-router-relay'

// history
import createHashHistory from 'history/lib/createHashHistory'

import routes from '../routes'

// setup history
const history = useRouterHistory(createHashHistory)({ queryKey: false })

export default class RouterElement extends Component {
  render () {
    return (
      <Router
        history={history}
        routes={routes}
        render={applyRouterMiddleware(useRelay)}/>
    )
  }
}
