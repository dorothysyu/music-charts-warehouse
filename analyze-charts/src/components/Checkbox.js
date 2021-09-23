import PropTypes from 'prop-types'

const Checkbox = ({ color, text, onClick }) => {

    return (
        <button className='btn' onClick={onClick} style={{ backgroundColor: color }}>
            {text}
        </button>
    )
}

Checkbox.defaultProps = {
    color: '#95a5a6',
}

Checkbox.propTypes = {
    text: PropTypes.string,
    color: PropTypes.string,
    onClick: PropTypes.func.isRequired
}

export default Checkbox
