import express from 'express';
import cors from 'cors';
import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// 数据文件路径
const dataDir = './data';
const propertiesFile = path.join(dataDir, 'properties.json');

// 确保数据目录存在
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// 加载房源数据
function loadProperties() {
  try {
    if (fs.existsSync(propertiesFile)) {
      const data = fs.readFileSync(propertiesFile, 'utf-8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('Failed to load properties:', error);
  }

  // 返回默认房源
  return [
    {
      id: '1',
      name: 'Modern Drouin Family Home | Long Stays Welcome',
      location: 'Drouin, Victoria, Australia',
      currency: 'AUD',
      pricePerNight: 400,
      peakSeasonPrice: 750,
      rating: 4.9,
      reviews: 48,
      images: [
        '/images/exterior.jpg',
        '/images/bedroom1.jpg',
        '/images/bedroom2.jpg',
        '/images/living-room.jpg',
        '/images/kitchen.jpg'
      ],
      description: 'Modern five-year-old, three-bedroom home designed for comfortable family and extended stays. Ideal for guests relocating during home repairs, families between homes, insurance-related accommodation and professionals working in Drouin or Warragul.',
      bedrooms: 3,
      bathrooms: 2,
      guests: 6,
      bedType: '1 Master + 2 Queen beds',
      amenities: ['WiFi', 'Full Kitchen', 'Hot Water Spa Bath', 'Free Parking', 'Washing Machine', 'Heating & Cooling', 'Pet Friendly', 'Waterfront Location'],
      minNights: 3,
      availableDates: {
        from: '2026-09-10',
        to: '2027-12-31'
      }
    }
  ];
}

// 保存房源数据
function saveProperties(props) {
  try {
    fs.writeFileSync(propertiesFile, JSON.stringify(props, null, 2), 'utf-8');
  } catch (error) {
    console.error('保存房源数据失败:', error);
  }
}

let properties = loadProperties();

// 预订记录（内存存储，可以替换为数据库）
let bookings = [];

// 获取所有房源
app.get('/api/properties', (req, res) => {
  // 重新加载以获取最新数据
  properties = loadProperties();
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

// 添加新房源
app.post('/api/properties', (req, res) => {
  const property = req.body;

  if (!property.name || !property.location || !property.pricePerNight) {
    return res.status(400).json({ error: '缺少必要的房源信息' });
  }

  // 确保ID唯一
  if (!property.id) {
    property.id = Date.now().toString();
  }

  // 如果相同ID已存在，更新它
  const index = properties.findIndex(p => p.id === property.id);
  if (index !== -1) {
    properties[index] = property;
  } else {
    properties.push(property);
  }

  saveProperties(properties);
  res.status(201).json(property);
});

// 删除房源
app.delete('/api/properties/:id', (req, res) => {
  const index = properties.findIndex(p => p.id === req.params.id);
  if (index !== -1) {
    const deleted = properties.splice(index, 1);
    saveProperties(properties);
    res.json({ message: '房源已删除', property: deleted[0] });
  } else {
    res.status(404).json({ error: '房源未找到' });
  }
});

// 更新房源
app.put('/api/properties/:id', (req, res) => {
  const index = properties.findIndex(p => p.id === req.params.id);
  if (index !== -1) {
    properties[index] = { ...properties[index], ...req.body };
    saveProperties(properties);
    res.json(properties[index]);
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
