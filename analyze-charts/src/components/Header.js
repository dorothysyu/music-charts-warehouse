import PropTypes from 'prop-types'
import Checkbox from './Checkbox'

const Header = ({ title }) => {

    const onClick = (e) => {
        console.log(e)

    }

    return (
        <header className='header'>
            <h1>{title}</h1>
            <Checkbox color='#95A5A6' text='Spotify' onClick={onClick} />
            <Checkbox color='#95A5A6' text='Billboard' onClick={onClick} />
        </header>
    )
}

Header.propTypes = {
    title: PropTypes.string, //.isRequired
}

export default Header



