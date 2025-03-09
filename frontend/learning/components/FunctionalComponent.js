import { useEffect, useState } from "react";

function FunctionalComponent() {
    console.log('[Function] Beginning');
    const [value, setValue] = useState(0);

    useEffect(() => {
        console.log('[Function] useEffect []');

    return () => {
        console.log(
            '[Function] useEffect return []'
        );
    };
}, []);
    useEffect(() => {
        console.log('[Function] useEffect [value]');

        return () => {
            console.log(
                '[Function] useEffect return [value]'
            );
        };
    }, [value]);

    console.log('[Function] End')

    return (
        <div>
            <h1>FunctionComponent</h1>
            <h1>value: {value}</h1>
            <button onClick={() => {
                setValue((state) => state + 1)
            }}>Increase value</button>
        </div>
    )
}

export default FunctionalComponent