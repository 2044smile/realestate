import React, { Component } from "react";  // Component 안에 내장 Hook 으로 useState 가 존재한다

export default class ClassState extends Component {
    state = {  // 멤버 변수 dict
        value: 0
    };

    // const [value, setValue] = useState(0);  함수형 컴포넌트 list

    constructor(props) {  // 생성자 => 컴포넌트가 만들어지면 생성된다 초기화
        super(props);
        this.state = {
            value: 1
        }
    }

    resetValue() {
        this.setState({ value : 0});
    }

    render() {
        return (
            <div>
                <h1>class state value: {this.state.value}</h1>
                <button onClick={() => {
                    this.setState((state) => ({  // this setState 라는 멤버 함수를 이용하여 state 전체 값을 세팅
                        value: state.value + 1  // setState 로 값이 변경된 것을 ClassState 에게 알리고, ClassState 는 상태가 변했기에 render 함수를 호출
                    }));
                }}>
                   Increase value 
                </button>
                <button onClick={this.resetValue.bind(this) // .bind(this) 필수
                    // this.setState((state) => ({
                    //      value: 0
                    // }));
                }>
                    Reset value
                </button>
            </div>
        )
    }
}