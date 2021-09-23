import PropTypes from 'prop-types'
import Button from './Checkbox'

const Header = ({ title }) => {

    const onClick = (e) => {
        console.log(e)

    }

    return (
        <header className='header'>
            <h1>{title}</h1>
            <Button color='#95A5A6' text='Spotify' onClick={onClick} />
            <Button color='#95A5A6' text='Billboard' onClick={onClick} />
        </header>
    )
}

Header.propTypes = {
    title: PropTypes.string, //.isRequired
}

export default Header



