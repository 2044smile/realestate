export default function Heading(props) {
    if(props.type === 'h3') {
        return <h3>{props.children}</h3>
    }
    
    return <h1>{props.children}</h1>
}