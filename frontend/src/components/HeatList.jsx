import React, { PropTypes, Component } from 'react'
import Relay from 'react-relay'

// TODO, make heat component
import Heat from './HeatListItem'

class HeatList extends Component {
  static propTypes = {
    viewer: React.PropTypes.object.isRequired
  }
  // constructor (props) {
  //   super(props)
  // }
  renderHeats () {
    return this.props.viewer.heats.edges.map(({ node }) =>
      <Heat
        key={node.uuid}
        heat={node}/>
    )
  }
  render () {
    // const { numHeats } = this.props.heats
    const {numHeats} = this.props.viewer
    return (
      <section className="heat-section">
        <span>number of heats: {numHeats}</span>
        <ui className="heat-list">
          {this.renderHeats()}
        </ui>
      </section>
    )
  }
}

// numHeats
export default Relay.createContainer(HeatList, {
  fragments: {
    viewer: () => Relay.QL`
      fragment on RaceQuery {
        numHeats
        heats: allHeats(first: 5) {
          edges {
            node {
              id
              uuid
              ${Heat.getFragment('heat')}
            }
          }
        }
      }
    `
  }
})
