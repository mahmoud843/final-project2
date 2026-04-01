const products = [
  {id:1, name:"تعلم Python للمبتدئين", category:"python", price:120, img:"python_book.png"},
  {id:2, name:"CSS من الصفر للاحتراف", category:"css", price:80, img:"css_book.png"},
  {id:3, name:"JavaScript كامل", category:"javascript", price:150, img:"js_book.png"},
  {id:4, name:"HTML & Web Design", category:"html", price:70, img:"html_book.png"}
];

let cart = [];

const productsGrid = document.getElementById('productsGrid');
const cartList = document.getElementById('cartList');
const cartCount = document.getElementById('cartCount');
const totalPriceEl = document.getElementById('totalPrice');

function renderProducts(filter="all"){
  productsGrid.innerHTML = '';
  const filtered = filter==="all" ? products : products.filter(p=>p.category===filter);
  filtered.forEach(p=>{
    const card = document.createElement('div');
    card.className = "card";
    card.innerHTML = `
      <div class="cover"><img src="${p.img}" alt="${p.name}" style="width:100%; height:100%; border-radius:16px;"></div>
      <div class="meta">
        <div class="price">${p.price} جنيه</div>
        <button class="addBtn" onclick="addToCart(${p.id})">أضف للسلة</button>
      </div>
    `;
    productsGrid.appendChild(card);
  });
}

function addToCart(id){
  const item = products.find(p=>p.id===id);
  const exist = cart.find(c=>c.id===id);
  if(exist) exist.qty++;
  else cart.push({...item, qty:1});
  updateCart();
}

function updateCart(){
  cartList.innerHTML='';
  let total = 0;
  cart.forEach((c,i)=>{
    total += c.price*c.qty;
    const div = document.createElement('div');
    div.className = "cartItem";
    div.innerHTML = `
      <div class="cartLeft">
        <div class="miniLogo"></div>
        <div class="cartTxt">
          <div class="t">${c.name}</div>
          <div class="p">${c.price} جنيه</div>
        </div>
      </div>
      <div class="cartControls">
        <button onclick="changeQty(${i},-1)">-</button>
        <div class="qty">${c.qty}</div>
        <button onclick="changeQty(${i},1)">+</button>
      </div>
    `;
    cartList.appendChild(div);
  });
  cartCount.innerText = cart.length;
  totalPriceEl.innerText = total;
}

function changeQty(i,delta){
  cart[i].qty += delta;
  if(cart[i].qty <=0) cart.splice(i,1);
  updateCart();
}
document.getElementById('searchInput').addEventListener('input', e => {
    const q = e.target.value.toLowerCase();

    productsGrid.innerHTML = "";

    const filtered = products.filter(p =>
        p.name.toLowerCase().includes(q)
    );

    filtered.forEach(p => {
        const card = document.createElement('div');
        card.className = "card";

        card.innerHTML = `
        <div class="cover">
            <img src="${p.img}" alt="${p.name}" style="width:100%">
        </div>
        <div class="meta">
            <div class="price">${p.price} جنيه</div>
            <button class="addBtn" onclick="addToCart(${p.id})">أضف للسلة</button>
        </div>
        `;

        productsGrid.appendChild(card);
    });
});
renderProducts();
