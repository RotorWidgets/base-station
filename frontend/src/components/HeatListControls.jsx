import React {Component} from 'react'
import Relay from 'react-relay'
import { IndexLink, Link } from 'react-router'

// HeatListControls lets you show only upcoming heats

class HeatListControls extends Component {
  static propTypes = {
    viewer: React.PropTypes.object.isRequired
  }

  render() {
    return (
      <header className="heat-list-controls">
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

export default Relay.createContainer(HeatListControls, {
  // prepareVariables() {
  //   return {
  //     limit: -1 >>> 1
  //   }
  // },
  // heats(status: "completed", first: $limit) {
  //   ${RemoveCompletedTodosMutation.getFragment('todos')}
  // },
  fragments: {
    viewer: () => Relay.QL`
      fragment on RaceQuery {
        numHeats,
        numUpcomingHeats,
        ${RemoveCompletedTodosMutation.getFragment('viewer')}
      }
    `
  }
})
