import React, { PropTypes } from 'react'
import Relay from 'react-relay'

class HeatApp extends React.Component {
  static PropTypes = {
    viewer: PropTypes.object,
    children: PropTypes.node.isRequired
  }

  render () {
    const { viewer, children } = this.props
    return (
      <section className="heat-app">
        <header>
          <h3>All Heats</h3>
        </header>
        {children}
      </section>
    )
  }
}

// $(HeatListHeader.getFragment('viewer'))
export default Relay.createContainer(HeatApp, {
  fragments: {
    viewer: () => Relay.QL`
      fragment on RaceQuery {
        numHeats
      }
    `
  }
})
