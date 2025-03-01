import './App.css';

const arr = ['10', '20', '30'];
const arr2 = [];

for (let i = 0; i < arr.length; i++) {
  arr2.push(<h4 key={i}>{arr[i]}</h4>);
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
      </header>
    </div>
  );
}

export default App;