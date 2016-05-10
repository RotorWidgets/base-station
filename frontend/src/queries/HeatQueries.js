import Relay from 'react-relay'


// `headId` receives a value from the route
export default {
  singleHeat: () => Relay.QL`
    query {
      heat(id: $heatId)
    }
  `
}
