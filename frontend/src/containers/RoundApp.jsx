import React, { PropTypes } from 'react'
import Relay from 'react-relay'

class RoundApp extends React.Component {
  static PropTypes = {
    viewer: PropTypes.object,
    children: PropTypes.node.isRequired
  }

  render () {
    const { viewer, children } = this.props
    return (
      <section className="round-app">
        <header>
          <h3>All Rounds</h3>
        </header>
        {children}
      </section>
    )
  }
}

// $(RoundListHeader.getFragment('viewer'))
export default Relay.createContainer(RoundApp, {
  fragments: {
    viewer: () => Relay.QL`
      fragment on RaceQuery {
        numRounds
      }
    `
  }
})
