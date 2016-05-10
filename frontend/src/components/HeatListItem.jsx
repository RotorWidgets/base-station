import React, { PropTypes } from 'react'
import Relay from 'react-relay'

class HeatListItem extends React.Component {
  static PropTypes = {
    heat: PropTypes.object.isRequired
  }
  render () {
    const { number, started, ended, startedTime, endedTime } = this.props.heat
    return (
      <li>
        <strong>Heat {number}</strong>
        <span>{(started) ? <time datetime={startedTime}>started</time> : ''}</span>
        <span>{(ended) ? <time datetime={endedTime}>ended</time> : ''}</span>
      </li>
    )
  }
}

export default Relay.createContainer(HeatListItem, {
  fragments: {
    // viewer: () => Relay.QL`
    //   fragment on User {
    //     ${ChangeTodoStatusMutation.getFragment('viewer')},
    //     ${RemoveTodoMutation.getFragment('viewer')}
    //   }
    // `,
    heat: () => Relay.QL`
      fragment on RaceHeat{
        id
        number
        uuid
        started
        startedTime
        ended
        endedTime
      }
    `
  }
})
// ${ChangeTodoStatusMutation.getFragment('todo')},
// ${RemoveTodoMutation.getFragment('todo')},
// ${RenameTodoMutation.getFragment('todo')}
