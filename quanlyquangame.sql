-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th7 07, 2024 lúc 09:03 PM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `quanlyquangame`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `chitiethoadondichvu`
--

CREATE TABLE `chitiethoadondichvu` (
  `id` int(11) NOT NULL,
  `hoa_don_id` int(11) NOT NULL,
  `dich_vu_id` int(11) NOT NULL,
  `so_luong` int(11) NOT NULL,
  `thanh_tien` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `chitiethoadondichvu`
--

INSERT INTO `chitiethoadondichvu` (`id`, `hoa_don_id`, `dich_vu_id`, `so_luong`, `thanh_tien`) VALUES
(90, 49, 6, 1, 7000),
(91, 49, 5, 1, 15000),
(92, 49, 9, 2, 16000),
(93, 50, 6, 1, 7000),
(94, 50, 9, 1, 8000),
(95, 50, 8, 1, 15000),
(96, 51, 6, 1, 7000),
(97, 51, 5, 1, 15000),
(98, 52, 6, 1, 7000),
(99, 52, 5, 1, 15000),
(100, 52, 2, 1, 15000),
(101, 53, 6, 1, 7000),
(102, 53, 5, 1, 15000),
(103, 54, 6, 1, 7000),
(104, 54, 5, 1, 15000),
(105, 54, 9, 1, 8000),
(106, 55, 6, 1, 7000),
(107, 55, 5, 1, 15000),
(108, 56, 6, 1, 7000),
(109, 56, 5, 1, 15000),
(110, 57, 6, 1, 7000),
(111, 58, 6, 1, 7000),
(112, 58, 9, 1, 8000),
(113, 58, 7, 1, 10000),
(114, 59, 6, 1, 7000),
(115, 59, 5, 1, 15000),
(116, 60, 6, 1, 7000),
(117, 60, 5, 1, 15000),
(118, 60, 9, 1, 8000),
(119, 61, 6, 1, 7000),
(120, 62, 6, 1, 7000),
(121, 63, 6, 1, 7000),
(122, 64, 6, 1, 7000),
(123, 64, 9, 1, 8000),
(124, 65, 6, 1, 7000),
(125, 65, 9, 2, 16000),
(126, 65, 8, 1, 15000),
(127, 66, 6, 1, 7000),
(128, 67, 6, 1, 7000),
(129, 68, 6, 1, 7000),
(130, 68, 6, 2, 14000),
(131, 69, 6, 1, 7000),
(132, 70, 6, 1, 7000),
(133, 71, 6, 1, 7000),
(134, 71, 5, 1, 15000),
(136, 72, 9, 1, 8000),
(137, 72, 5, 1, 15000),
(138, 73, 9, 1, 8000),
(139, 73, 8, 1, 15000),
(141, 74, 6, 1, 7000),
(142, 74, 5, 1, 15000),
(146, 76, 6, 1, 7000),
(147, 76, 9, 1, 8000),
(150, 78, 6, 1, 7000),
(151, 77, 6, 1, 7000),
(152, 77, 5, 1, 15000),
(156, 80, 6, 1, 7000),
(157, 80, 5, 1, 15000),
(158, 81, 6, 1, 7000),
(159, 81, 5, 1, 15000),
(160, 82, 6, 1, 7000),
(161, 82, 9, 1, 8000),
(162, 83, 6, 1, 7000),
(163, 83, 5, 1, 15000),
(164, 84, 6, 1, 7000),
(165, 84, 5, 1, 15000),
(166, 85, 6, 1, 7000),
(167, 85, 5, 1, 15000),
(168, 85, 4, 1, 3000),
(169, 86, 6, 1, 7000),
(170, 86, 5, 1, 15000),
(171, 86, 8, 1, 15000),
(172, 87, 6, 1, 7000),
(173, 87, 9, 1, 8000),
(174, 88, 6, 1, 7000),
(175, 88, 9, 1, 8000),
(176, 88, 8, 1, 15000),
(177, 88, 4, 1, 3000);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `dichvu`
--

CREATE TABLE `dichvu` (
  `dich_vu_id` int(11) NOT NULL,
  `ten_dich_vu` varchar(100) NOT NULL,
  `anh_dich_vu` varchar(100) DEFAULT NULL,
  `gia` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `dichvu`
--

INSERT INTO `dichvu` (`dich_vu_id`, `ten_dich_vu`, `anh_dich_vu`, `gia`) VALUES
(1, '20 gói tăm cay que cay', 'tamcay.jpg', 30000),
(2, '500G Bim Bim Tăm Đậu Hà Lan, Snack Que Bim Tăm Thái, đồ ăn vặt hot, đồ 1k', 'que.jpg', 15000),
(3, 'Bim Bim Cà Chua Khổng Lồ', 'vn-11134207-7r98o-ltqgfpzxx1cdfc.jpg', 45000),
(4, 'Snack bim bim cánh gà chiên giòn (gói 26g)', '0b2111257ff7cb12ffad61017c47c0a7.jpg', 3000),
(5, 'Snack bim bim que Mix Vfoods 50g', '15a3ae66e37d204e34899af807b05050.jpg', 15000),
(6, 'Oishi- Snack cay tôm', 'vn-11134207-7r98o-lnmfl6k7wjqlf1.jpg', 7000),
(7, 'Combo oishi', 'vn-11134207-7r98o-lnmfl6k7bh7xe6.jpg', 10000),
(8, 'Nước Ép Táo Xanh AUFINE 150ml', 'sg-11134201-23020-cjld23i8fdnv47.jpg', 15000),
(9, 'CoCa CoLa', 'vn-11134207-7r98o-lw7f2ff9vbvdd6.jpg', 8000),
(10, 'Sting', 'sg-11134201-22110-qcdc1e95g5jv1e.jpg', 15000),
(11, 'Mirinda', 'vn-11134207-7r98o-lptal6stjy6qb2.jpg', 15000),
(12, 'Nước cốt hoa Atiso đỏ BerryLand chai 500ml', '4874b2f865e536938bc7dfc0adbcd665.jpg', 39000);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `hoadon`
--

CREATE TABLE `hoadon` (
  `hoadon_id` int(11) NOT NULL,
  `nguoi_dung_id` int(11) NOT NULL,
  `may_id` int(11) NOT NULL,
  `thoi_gian_bat_dau` datetime NOT NULL,
  `thoi_gian_ket_thuc` datetime DEFAULT NULL,
  `tong_tien` float DEFAULT NULL,
  `trang_thai_hoa_don` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `hoadon`
--

INSERT INTO `hoadon` (`hoadon_id`, `nguoi_dung_id`, `may_id`, `thoi_gian_bat_dau`, `thoi_gian_ket_thuc`, `tong_tien`, `trang_thai_hoa_don`) VALUES
(49, 2, 1, '2024-07-07 09:00:47', '2024-07-07 09:36:47', 45000, 1),
(50, 5, 2, '2024-07-06 09:01:28', '2024-07-06 21:01:28', 114000, 1),
(51, 2, 2, '2024-07-06 09:02:04', '2024-07-06 21:02:04', 106000, 1),
(52, 2, 2, '2024-07-06 09:02:36', '2024-07-06 12:02:36', 58000, 1),
(53, 2, 3, '2024-07-07 09:03:11', '2024-07-07 21:03:11', 106000, 1),
(54, 2, 1, '2024-07-07 09:41:39', '2024-07-07 09:45:39', 30490, 1),
(55, 2, 1, '2024-07-07 09:42:43', '2024-07-07 09:45:43', 22350, 1),
(56, 2, 1, '2024-07-07 09:46:50', '2024-07-07 09:50:50', 22490, 1),
(57, 2, 1, '2024-07-07 09:52:38', '2024-07-07 09:55:38', 7350, 1),
(58, 2, 5, '2024-07-07 09:52:38', '2024-07-07 10:52:38', 32000, 1),
(59, 2, 4, '2024-07-07 09:57:36', '2024-07-07 10:57:36', 29000, 1),
(60, 2, 1, '2024-07-07 15:47:14', '2024-07-07 15:48:14', 30140, 1),
(61, 5, 2, '2024-07-07 15:50:22', '2024-07-07 16:00:22', 8190, 1),
(62, 5, 4, '2024-07-07 15:56:13', '2024-07-07 15:57:13', 7140, 1),
(63, 2, 1, '2024-07-07 16:03:33', '2024-07-07 16:04:33', 7140, 1),
(64, 2, 2, '2024-07-07 16:30:52', '2024-07-07 23:30:52', 64000, 1),
(65, 2, 3, '2024-07-07 23:35:11', '2024-07-07 23:55:11', 40800, 1),
(66, 2, 4, '2024-07-07 23:37:27', '2024-07-07 23:57:27', 9310, 1),
(68, 2, 5, '2024-07-07 23:37:47', '2024-07-07 23:57:47', 23310, 1),
(69, 2, 3, '2024-07-08 00:00:23', '2024-07-08 00:01:23', 7140, 1),
(70, 2, 3, '2024-07-08 00:01:34', '2024-07-08 00:02:34', 7140, 1),
(71, 5, 4, '2024-07-08 00:01:52', '2024-07-08 00:03:52', 22210, 1),
(72, 5, 5, '2024-07-08 00:05:21', '2024-07-08 10:05:21', 93000, 1),
(73, 2, 4, '2024-07-08 00:05:41', '2024-07-08 01:05:41', 30000, 1),
(74, 2, 3, '2024-07-08 00:07:20', '2024-07-08 00:09:20', 22210, 1),
(76, 2, 9, '2024-07-08 00:14:21', '2024-07-08 00:20:21', 15900, 1),
(77, 2, 10, '2024-07-08 00:25:01', '2024-07-08 00:30:01', 22720, 1),
(78, 2, 10, '2024-07-08 00:31:48', '2024-07-08 00:38:48', 8080, 1),
(80, 2, 10, '2024-07-08 00:50:30', '2024-07-08 00:55:30', 22720, 1),
(81, 2, 15, '2024-07-08 00:56:07', '2024-07-08 00:59:07', 22500, 1),
(82, 2, 10, '2024-07-08 01:19:46', '2024-07-08 01:20:46', 15180, 1),
(83, 5, 10, '2024-07-08 01:23:58', '2024-07-08 01:25:58', 22270, 1),
(84, 2, 14, '2024-07-08 01:31:50', '2024-07-08 01:32:50', 22200, 1),
(85, 2, 10, '2024-07-08 01:44:47', '2024-07-08 01:45:47', 25180, 1),
(86, 2, 22, '2024-07-08 01:49:30', '2024-07-08 01:52:30', 37600, 1),
(87, 5, 26, '2024-07-08 01:50:06', '2024-07-08 01:55:06', 16200, 1),
(88, 2, 24, '2024-07-08 01:55:46', '2024-07-08 01:56:46', 33240, 1);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `maytram`
--

CREATE TABLE `maytram` (
  `may_id` int(11) NOT NULL,
  `ten_may` varchar(50) NOT NULL,
  `trang_thai` varchar(20) NOT NULL,
  `mo_ta` text DEFAULT NULL,
  `may_don_gia` int(11) DEFAULT NULL,
  `anh_may` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `maytram`
--

INSERT INTO `maytram` (`may_id`, `ten_may`, `trang_thai`, `mo_ta`, `may_don_gia`, `anh_may`) VALUES
(1, 'Máy 1', 'Đang nghỉ', 'Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm', 7000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(2, 'Máy 2', 'Đang nghỉ', 'Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm', 7000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(3, 'Máy 3', 'Đang nghỉ', 'Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm', 7000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(4, 'Máy 4', 'Đang nghỉ', 'Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm', 7000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(5, 'Máy 5', 'Hoạt động', 'Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm', 7000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(6, 'Máy 6', 'Đang nghỉ', 'LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12', 9000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(7, 'Máy 7', 'Đang nghỉ', 'LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12', 9000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(8, 'Máy 8', 'Đang nghỉ', 'LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12', 9000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(9, 'Máy 9', 'Đang nghỉ', 'LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12', 9000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(10, 'Máy 10', 'Đang nghỉ', 'LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12', 9000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(11, 'Máy 11', 'Đang nghỉ', 'LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT', 10000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(12, 'Máy 12', 'Đang nghỉ', 'LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT', 10000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(13, 'Máy 13', 'Đang nghỉ', 'LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT', 10000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(14, 'Máy 14', 'Đang nghỉ', 'LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT', 10000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(15, 'Máy 15', 'Đang nghỉ', 'LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT', 10000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(16, 'Máy 16', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(17, 'Máy 17', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(18, 'Máy 18', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'phancungcobantrenmaytinh1-1614184775.jpg'),
(19, 'Máy 19', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(20, 'Máy 20', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(21, 'Máy 21', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(22, 'Máy 22', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(23, 'Máy 23', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(24, 'Máy 24', 'Đang nghỉ', 'Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301', 12000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(25, 'Máy 25', 'Đang nghỉ', '27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403', 15000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(26, 'Máy 26', 'Đang nghỉ', '27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403', 15000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(27, 'Máy 27', 'Đang nghỉ', '27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403', 15000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(28, 'Máy 28', 'Đang nghỉ', '27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403', 15000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(29, 'Máy 29', 'Đang nghỉ', '27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403', 15000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(30, 'Máy 30', 'Đang nghỉ', '27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403', 15000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(31, 'Máy 31', 'Đang nghỉ', ' 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực', 18000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(32, 'Máy 32', 'Đang nghỉ', ' 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực', 18000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(33, 'Máy 33', 'Đang nghỉ', ' 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực', 18000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(34, 'Máy 34', 'Đang nghỉ', ' 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực', 18000, 'may-tinh-quan-net-thanh-ly-4.jpg'),
(35, 'Máy 35', 'Đang nghỉ', ' 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực', 18000, 'may-tinh-quan-net-thanh-ly-4.jpg');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `nguoidung`
--

CREATE TABLE `nguoidung` (
  `nguoi_dung_id` int(11) NOT NULL,
  `ten` varchar(100) NOT NULL,
  `tai_khoan` varchar(50) NOT NULL,
  `mat_khau` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `so_dien_thoai` varchar(15) DEFAULT NULL,
  `so_tien` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `nguoidung`
--

INSERT INTO `nguoidung` (`nguoi_dung_id`, `ten`, `tai_khoan`, `mat_khau`, `email`, `so_dien_thoai`, `so_tien`) VALUES
(2, 'minh tùng', 'mt', '1', 'mtung@gmail.com', '0329723748', 972930),
(4, 'minh tùng', 'mt1', '1', 'mtung@gmail.com', '0329723748', 50000),
(5, 'minh tùng', 'mt2', '1', 'mtung@gmail.com', '0329723748', 6491005);

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `chitiethoadondichvu`
--
ALTER TABLE `chitiethoadondichvu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hoa_don_id` (`hoa_don_id`),
  ADD KEY `dich_vu_id` (`dich_vu_id`);

--
-- Chỉ mục cho bảng `dichvu`
--
ALTER TABLE `dichvu`
  ADD PRIMARY KEY (`dich_vu_id`);

--
-- Chỉ mục cho bảng `hoadon`
--
ALTER TABLE `hoadon`
  ADD PRIMARY KEY (`hoadon_id`),
  ADD KEY `nguoi_dung_id` (`nguoi_dung_id`),
  ADD KEY `may_id` (`may_id`);

--
-- Chỉ mục cho bảng `maytram`
--
ALTER TABLE `maytram`
  ADD PRIMARY KEY (`may_id`);

--
-- Chỉ mục cho bảng `nguoidung`
--
ALTER TABLE `nguoidung`
  ADD PRIMARY KEY (`nguoi_dung_id`),
  ADD UNIQUE KEY `tai_khoan` (`tai_khoan`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `chitiethoadondichvu`
--
ALTER TABLE `chitiethoadondichvu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=178;

--
-- AUTO_INCREMENT cho bảng `dichvu`
--
ALTER TABLE `dichvu`
  MODIFY `dich_vu_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT cho bảng `hoadon`
--
ALTER TABLE `hoadon`
  MODIFY `hoadon_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT cho bảng `maytram`
--
ALTER TABLE `maytram`
  MODIFY `may_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT cho bảng `nguoidung`
--
ALTER TABLE `nguoidung`
  MODIFY `nguoi_dung_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `chitiethoadondichvu`
--
ALTER TABLE `chitiethoadondichvu`
  ADD CONSTRAINT `chitiethoadondichvu_ibfk_1` FOREIGN KEY (`hoa_don_id`) REFERENCES `hoadon` (`hoadon_id`),
  ADD CONSTRAINT `chitiethoadondichvu_ibfk_2` FOREIGN KEY (`dich_vu_id`) REFERENCES `dichvu` (`dich_vu_id`);

--
-- Các ràng buộc cho bảng `hoadon`
--
ALTER TABLE `hoadon`
  ADD CONSTRAINT `hoadon_ibfk_1` FOREIGN KEY (`nguoi_dung_id`) REFERENCES `nguoidung` (`nguoi_dung_id`),
  ADD CONSTRAINT `hoadon_ibfk_2` FOREIGN KEY (`may_id`) REFERENCES `maytram` (`may_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
