import { useState } from "react";

export default function State() {  // 2. 상태가 변화 되었으므로 함수 자체를 한번 더 돌린다
    // let value = 0;
    const [value, setValue] = useState(0);  // setValue == setter useState(초기값)

    return (
        <div>
            <h1>function state value: {value}</h1>
            <button onClick={() => {
                setValue(value + 1);  // 1. 값이 증가가 되면 State Component 에게 전달한다.
            }}>
                Increase value
            </button>
            <button onClick={() => {
                setValue(0);
            }}>
                Reset value
            </button>
        </div>
    )
}