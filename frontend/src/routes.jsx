// import Relay from 'react-relay'
import React from 'react'

import { IndexRoute, Route } from 'react-router'

import ViewerQueries from './queries/ViewerQueries'
// import HeatQueries from './queries/HeatQueries'

import HeatApp from './containers/HeatApp'
import HeatList from './components/HeatList'

// path='/heats'
// prepareParams={() => ({race: 'race_id'})}
// TODO: add a route to filter heats by a particular race
// let IndexQuery = Relay.QL`query { viewer }`

export default (
  <Route
    path='/'
    component={HeatApp}
    queries={ViewerQueries}
  >
    <IndexRoute
      component={HeatList}
      queries={ViewerQueries}
    />
    <Route
      path=':heatId'
      component={HeatList}
      queries={ViewerQueries}
    />
  </Route>
)
