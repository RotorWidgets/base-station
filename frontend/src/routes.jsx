// import Relay from 'react-relay'
import React from 'react'

import { IndexRoute, Route } from 'react-router'

import ViewerQueries from './queries/ViewerQueries'
// import RoundQueries from './queries/RoundQueries'

import RoundApp from './containers/RoundApp'
import RoundList from './components/RoundList'

// path='/rounds'
// prepareParams={() => ({race: 'race_id'})}
// TODO: add a route to filter rounds by a particular race
// let IndexQuery = Relay.QL`query { viewer }`

export default (
  <Route
    path='/'
    component={RoundApp}
    queries={ViewerQueries}
  >
    <IndexRoute
      component={RoundList}
      queries={ViewerQueries}
    />
    <Route
      path=':roundId'
      component={RoundList}
      queries={ViewerQueries}
    />
  </Route>
)
