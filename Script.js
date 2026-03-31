fetch('http://localhost:5000/projects')
.then(res=>res.json())
.then(data=>{
 const container=document.getElementById('container');
 data.forEach(p=>{
  const div=document.createElement('div');
  div.className='card';
  div.innerHTML=`
    <img src="http://localhost:5000/${p.image}" width="100%">
    <h3>${p.title}</h3>
    <p>${p.desc}</p>
  `;
  container.appendChild(div);
 });
});