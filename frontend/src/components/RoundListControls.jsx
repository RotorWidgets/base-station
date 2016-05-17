import React {Component} from 'react'
import Relay from 'react-relay'
import { IndexLink, Link } from 'react-router'

// RoundListControls lets you show only upcoming rounds

class RoundListControls extends Component {
  static propTypes = {
    viewer: React.PropTypes.object.isRequired
  }

  render() {
    return (
      <header className="round-list-controls">
        {this.render}
        <ui className="filters">
          <li>
            <IndexLink to="/" activeClassName="selected">All</IndexLink>
          </li>
          <li>
            <Link to="/upcoming" activeClassName="selected"></Link>
          </li>
        </ui>
      </header>
    )
  }
}

export default Relay.createContainer(RoundListControls, {
  // prepareVariables() {
  //   return {
  //     limit: -1 >>> 1
  //   }
  // },
  // rounds(status: "completed", first: $limit) {
  //   ${RemoveCompletedTodosMutation.getFragment('todos')}
  // },
  fragments: {
    viewer: () => Relay.QL`
      fragment on RaceQuery {
        numRounds,
        numUpcomingRounds,
        ${RemoveCompletedTodosMutation.getFragment('viewer')}
      }
    `
  }
})
