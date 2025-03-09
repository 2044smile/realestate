import '../styles/CourseCard.css'


function CourseCard({img, tags, title, salePercent, monthlyPrice, installmentMonth, types}) {
    return (
    <div className="CourseCard">
        <div className="cover">
            <img alt="" src={img}/>
        </div>
        <div className="info">
            <ul class="tags">
                {tags.map((item, index) => (
                    <li key={index} class="tag">{item}</li>
                ))}
            </ul>
            <h4 className="name">{title}</h4>
            <div className="prices">
                <span className="sale-percent">{salePercent.toLocaleString()}</span>
                <span className="monthly-price">{monthlyPrice}</span>
                <span className="installment-month">{installmentMonth}</span>
            </div>
            <ul className="types">
                {types.map((item, index) => (
                    <li key={index} className={types}>{item}</li>
                ))}
            </ul>
        </div>
    </div>
    )
}

export default CourseCard