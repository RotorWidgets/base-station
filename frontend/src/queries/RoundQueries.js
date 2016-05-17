import Relay from 'react-relay'


// `headId` receives a value from the route
export default {
  singleRound: () => Relay.QL`
    query {
      round(id: $roundId)
    }
  `
}
