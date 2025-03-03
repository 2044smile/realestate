import './App.css'
import Heading from './components/Heading';
import Hello from './components/Hello'
import World from './components/World'

const arr = ['10', '20', '30'];
const arr2 = [];

for (let i = 0; i < arr.length; i++) {
  arr2.push(<h4 key={i}>{arr[i]}</h4>);
}

// 구구단
const num = [1,2,3,4,5,6,7,8,9];

const element = (  
  <div style={{ display: 'flex'}}>
    {num.map(
      (n) =>  // 조건문
        n >= 2 &&
        n !== 5 && (
          <div style={{  // JSX {{}}
            padding: 10,
            color: n % 2 ? 'blue' : 'black' // 조건문 2 % 2 = 0 나머지가 0 이면 False('black')
          }}
          >
            {num.map((m) => (
              <div>
                {n} x {m} = {n * m}
              </div>
            ))}
          </div>
       )
    )}
  </div>
);

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
        <Heading type="h3">Heading</Heading>
        <Hello />
        <World />
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
          <div>  
            {/* 
              구구단 
              단, 5단은 제외합니다.
              홀수 단은 다른 색으로 표시합니다.
              구구단은 오른쪽으로 나열되도록 합니다.
            */} 
              {element}
            </div>
          </div> 
        </div>
      </header>
    </div>
  );
}

export default App;