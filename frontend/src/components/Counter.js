import { useCallback, useEffect, useState } from 'react';


function Counter() {
    console.log('Render Counter')

    const [value, setValue] = useState(0); // State의 초기 값 0
    // value 가 변경될 때 마다 re-rendering 작업

    // useEffect(() => {  // 컴포넌트가 렌더링 될 때 현재 상태에 변화에 따라서 조건적으로 특정 작업을 실행하기 위한 Hook
    //     console.log(
    //         '[Function] useEffect []: 컴포넌트가 마운트 될 때, 한 번만!'
    //     );
        // const eventHandler = () => {
        //     console.log('click body');
        // }
        // document.body.addEventListener(
        //     'click',
        //     eventHandler
        // );

    //     return () => {  // clean up 기능
    //         console.log(
    //             '[Function] useEffect return []: 컴포넌트가 언마운트 될 때,'
    //         );
            // document.body.removeEventListener(
            //     'click',
            //     eventHandler
            // )
    //     };
    // }, []);

    useEffect(() => {
        console.log(
            '[Function] useEffect [value]: 컴포넌트가 마운트 될 떄, + value 가 변경되면'
        );
        const eventHandler = () => {
            console.log('click body');
        };
        document.body.addEventListener(
            'click',
            eventHandler
        );

        return () => {
            console.log(
                '[Function] useEffect return [value]: 세트 useEffect를 수행하기 전에,'
            );
            document.body.removeEventListener(
                'click',
                eventHandler
            );
        }}, [value]); // useState 의 value 가 변경되는 순간에 useEffect 를 실행한다
        
        const increaseValue = useCallback(() => {  // 리랜더링이 발생해도, useCallback 안에 있는 함수는 다시 만들지 않고, 재활용 한다
            setValue(value + 1);
        }, [value]);

        return (
            <div>
                <h1>value : {value}</h1>
                <button onClick={increaseValue}>Increase value</button>
            </div>
        )
    }

export default Counter