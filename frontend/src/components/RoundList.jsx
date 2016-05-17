import React, { PropTypes, Component } from 'react'
import Relay from 'react-relay'

// TODO, make round component
import Round from './RoundListItem'

class RoundList extends Component {
  static propTypes = {
    viewer: React.PropTypes.object.isRequired
  }
  // constructor (props) {
  //   super(props)
  // }
  renderRounds () {
    return this.props.viewer.rounds.edges.map(({ node }) =>
      <Round
        key={node.uuid}
        round={node}/>
    )
  }
  render () {
    // const { numRounds } = this.props.rounds
    const {numRounds} = this.props.viewer
    return (
      <section className="round-section">
        <span>number of rounds: {numRounds}</span>
        <ui className="round-list">
          {this.renderRounds()}
        </ui>
      </section>
    )
  }
}

// numRounds
export default Relay.createContainer(RoundList, {
  fragments: {
    viewer: () => Relay.QL`
      fragment on RaceQuery {
        numRounds
        rounds: allRounds(first: 5) {
          edges {
            node {
              id
              uuid
              ${Round.getFragment('round')}
            }
          }
        }
      }
    `
  }
})
