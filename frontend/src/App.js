import CourseCard from './components/CourseCard.js';


function App() {
  return (
    <div style={{ padding: 30}}>
      <CourseCard 
        img="https://dst6jalxvbuf5.cloudfront.net/media/images/Course/cover_image/221020_172526/%E1%84%8F%E1%85%A9%E1%84%89%E1%85%B3%E1%84%8F%E1%85%A1%E1%84%83%E1%85%B3_%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%E1%84%8B%E1%85%A8%E1%84%8C%E1%85%A5%E1%86%BC_PC.png"
        tags={['커머스', '자기개발', 'SNS']}
        title="평범한 당신의 인생을 바꾸는 치트키! 월 천+ 버는 퍼스널브랜딩"
        salePercent={16583}
        monthlyPrice="51%↓"
        installmentMonth="/ 12개월"
        types={['동영상 강의']}
      />  
    </div>
  )
}

export default App