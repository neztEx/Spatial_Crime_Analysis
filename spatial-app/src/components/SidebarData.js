import { FaHome, FaMapMarkedAlt, FaDatabase } from "react-icons/fa";
import React from 'react'

export const SidebarData = [
  {
    title: 'Home',
    path: '/',
    icon: <FaHome />,
    cName: 'nav-text'
  },
  {
    title: 'Data Overview',
    path: '/overview',
    icon: <FaDatabase />,
    cName: 'nav-text'
  },
  {
    title: 'Data Visualization',
    path: '/map',
    icon: <FaMapMarkedAlt />,
    cName: 'nav-text'
  }
]
