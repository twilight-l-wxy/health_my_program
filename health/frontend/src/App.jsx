import React from 'react';
import { Layout, Menu, theme } from 'antd';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { HomeOutlined, MedicineBoxOutlined, UserOutlined, DashboardOutlined } from '@ant-design/icons';

// 页面组件（实际开发中应该从单独的文件导入）
const HomePage = () => (
  <div style={{ padding: '24px' }}>
    <h1>欢迎使用智医通</h1>
    <p>智医通是一个基于人工智能的症状自查平台，旨在提高基层医疗机构的问诊效率和准确率。</p>
    <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '40px' }}>
      <div className="feature-card">
        <MedicineBoxOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
        <h2>症状自查</h2>
        <p>通过AI辅助，快速识别症状并获取初步诊断建议</p>
      </div>
      <div className="feature-card">
        <DashboardOutlined style={{ fontSize: '48px', color: '#52c41a' }} />
        <h2>风险评估</h2>
        <p>基于贝叶斯网络的疾病概率计算，提供科学的风险评估</p>
      </div>
      <div className="feature-card">
        <UserOutlined style={{ fontSize: '48px', color: '#722ed1' }} />
        <h2>分诊建议</h2>
        <p>智能推荐就诊科室和就医级别，提高就医效率</p>
      </div>
    </div>
  </div>
);

const SymptomCheckPage = () => (
  <div style={{ padding: '24px' }}>
    <h1>症状自查</h1>
    <p>请描述您的症状，我们将为您提供初步的诊断建议。</p>
    {/* 这里将来会添加症状输入表单和问诊流程组件 */}
  </div>
);

const UserProfilePage = () => (
  <div style={{ padding: '24px' }}>
    <h1>个人中心</h1>
    <p>管理您的个人信息和健康档案。</p>
    {/* 这里将来会添加用户资料管理组件 */}
  </div>
);

const App = () => {
  const { Header, Content, Footer, Sider } = Layout;
  const navigate = useNavigate();
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '首页',
    },
    {
      key: '/symptom-check',
      icon: <MedicineBoxOutlined />,
      label: '症状自查',
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: '个人中心',
    },
  ];

  const handleMenuClick = (e) => {
    navigate(e.key);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div className="logo" style={{ color: 'white', fontSize: '20px', fontWeight: 'bold', marginRight: '20px' }}>
          智医通
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['/']}
          items={menuItems}
          onClick={handleMenuClick}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: '0 50px' }}>
        <div
          style={{
            padding: 24,
            minHeight: 380,
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
            marginTop: '16px',
          }}
        >
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/symptom-check" element={<SymptomCheckPage />} />
            <Route path="/profile" element={<UserProfilePage />} />
          </Routes>
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        智医通 ©{new Date().getFullYear()} 基于人工智能的症状自查平台
      </Footer>
    </Layout>
  );
};

export default App;