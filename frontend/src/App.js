import './App.css'

const arr = ['10', '20', '30'];
const arr2 = [];

for (let i = 0; i < arr.length; i++) {
  arr2.push(<h4 key={i}>{arr[i]}</h4>);
}

// 2. style 재활용
const roundBoxStyle = {
  position: 'absolute',
  top: 50,
  left: 50,
  width: '50%',
  height: '200px',
  padding: 20,
  background: 'rgba(162, 216, 235, 0.6)',
  // 3. style - 속성은 camelCase
  borderRadius: 50  // border-radius
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Hello, world</h1>
        <h2>배열로 넣기</h2>
        <ul>
          <li>{arr}</li>  {/* 102030 */}
          <li>{arr2}</li>  {/* 반복문 */}
        </ul>
        <h2>Array.map</h2>
        <ul>
          <li>
            {arr.map((item, index) => {
              return <h4 key={index}>{item}</h4>
            })}
          </li>
        </ul>
        {/* 1. style - Object 로 css 작성 */}
        <div style={{
          position: 'relative',
          with: 400,
          height: 1000,
          background: '#f1f1f1'
        }}> {/* 첫 번째 {} -> JSX 에서 Javascript 표현식을 사용 할 때 필요, 두 번째 {} -> Javascript 객체를 정의 */} 
          <div style={roundBoxStyle}>Hello 1</div> 

          <div style={{ ...roundBoxStyle, top: 350}}>
            <div className={"highlight"}>Hello 2</div>  {/* "highlight" 보다 {"highlight"} 하면 JSX 방식으로 사용 */} 
          </div>
          <div style={{ ...roundBoxStyle, top: 650}}>
            {/* 5. style - 조건적 스타일 */} 
            <div 
              className={
                1 + 1 === 2 ? 'highlight' : false  
                // 1 + 1 == 2 && 'highlight' : false
              } 
            > {/* 삼항연산자, 앞에 내용이 참이면 'highlight' 거짓이면 className을 false */} 
              Hello 3
            </div>
          </div> 
        </div>
      </header>
    </div>
  );
}

export default App;