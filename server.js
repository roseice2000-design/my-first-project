import express from 'express';
import cors from 'cors';
import { v4 as uuidv4 } from 'uuid';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// 示例房源数据
const properties = [
  {
    id: '1',
    name: '温馨一卧室公寓',
    location: '市中心',
    price: 1200,
    currency: 'CNY',
    pricePerNight: 120,
    rating: 4.8,
    reviews: 125,
    image: '/images/property1.jpg',
    description: '舒适的一卧室公寓，靠近公共交通',
    bedrooms: 1,
    bathrooms: 1,
    guests: 2,
    amenities: ['WiFi', '空调', '厨房', '停车场'],
    availableDates: {
      from: '2026-09-10',
      to: '2026-12-31'
    }
  },
  {
    id: '2',
    name: '豪华两卧室别墅',
    location: '风景区',
    price: 2500,
    currency: 'CNY',
    pricePerNight: 250,
    rating: 4.9,
    reviews: 89,
    image: '/images/property2.jpg',
    description: '带花园和山景的豪华别墅',
    bedrooms: 2,
    bathrooms: 2,
    guests: 4,
    amenities: ['WiFi', '游泳池', '花园', '停车场', '空调', '厨房'],
    availableDates: {
      from: '2026-09-15',
      to: '2026-12-31'
    }
  }
];

// 预订记录（内存存储，可以替换为数据库）
let bookings = [];

// 获取所有房源
app.get('/api/properties', (req, res) => {
  res.json(properties);
});

// 获取单个房源详情
app.get('/api/properties/:id', (req, res) => {
  const property = properties.find(p => p.id === req.params.id);
  if (property) {
    res.json(property);
  } else {
    res.status(404).json({ error: '房源未找到' });
  }
});

// 获取预订详情
app.get('/api/bookings/:id', (req, res) => {
  const booking = bookings.find(b => b.id === req.params.id);
  if (booking) {
    res.json(booking);
  } else {
    res.status(404).json({ error: '预订未找到' });
  }
});

// 创建预订
app.post('/api/bookings', (req, res) => {
  const { propertyId, checkIn, checkOut, guests, fullName, email, phone } = req.body;

  if (!propertyId || !checkIn || !checkOut || !guests || !fullName || !email) {
    return res.status(400).json({ error: '缺少必要信息' });
  }

  const property = properties.find(p => p.id === propertyId);
  if (!property) {
    return res.status(404).json({ error: '房源未找到' });
  }

  // 计算天数和总价
  const start = new Date(checkIn);
  const end = new Date(checkOut);
  const nights = (end - start) / (1000 * 60 * 60 * 24);

  if (nights <= 0) {
    return res.status(400).json({ error: '退房日期必须在入住日期之后' });
  }

  const totalPrice = nights * property.pricePerNight;

  const booking = {
    id: uuidv4(),
    propertyId,
    propertyName: property.name,
    checkIn,
    checkOut,
    nights,
    guests,
    fullName,
    email,
    phone,
    totalPrice,
    currency: property.currency,
    status: 'confirmed',
    createdAt: new Date().toISOString(),
    confirmationCode: Math.random().toString(36).substring(2, 10).toUpperCase()
  };

  bookings.push(booking);
  res.status(201).json(booking);
});

// 获取所有预订（用于管理面板）
app.get('/api/bookings', (req, res) => {
  res.json(bookings);
});

// 取消预订
app.delete('/api/bookings/:id', (req, res) => {
  const index = bookings.findIndex(b => b.id === req.params.id);
  if (index !== -1) {
    const cancelled = bookings.splice(index, 1);
    res.json({ message: '预订已取消', booking: cancelled[0] });
  } else {
    res.status(404).json({ error: '预订未找到' });
  }
});

app.listen(PORT, () => {
  console.log(`🏠 房源预订网站运行在 http://localhost:${PORT}`);
});
