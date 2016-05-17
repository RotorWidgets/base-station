import React, { PropTypes } from 'react'
import Relay from 'react-relay'

class RoundListItem extends React.Component {
  static PropTypes = {
    round: PropTypes.object.isRequired
  }
  render () {
    const { number, started, ended, startedTime, endedTime } = this.props.round
    return (
      <li>
        <strong>Round {number}</strong>
        <span>{(started) ? <time datetime={startedTime}>started</time> : ''}</span>
        <span>{(ended) ? <time datetime={endedTime}>ended</time> : ''}</span>
      </li>
    )
  }
}

export default Relay.createContainer(RoundListItem, {
  fragments: {
    // viewer: () => Relay.QL`
    //   fragment on User {
    //     ${ChangeTodoStatusMutation.getFragment('viewer')},
    //     ${RemoveTodoMutation.getFragment('viewer')}
    //   }
    // `,
    round: () => Relay.QL`
      fragment on Round{
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
