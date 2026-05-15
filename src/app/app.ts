import { CommonModule } from '@angular/common';
import { Component, computed, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

type Gender = 'Men' | 'Women';
type Section = 'home' | 'men' | 'women' | 'cart' | 'orders';

interface Product {
  id: number;
  name: string;
  gender: Gender;
  collection: string;
  price: number;
  img: string;
}

interface CartItem {
  id: number;
  name: string;
  price: number;
  qty: number;
}

interface CheckoutDetails {
  name: string;
  email: string;
  phone: string;
  address: string;
}

interface Order {
  orderId: number;
  items: CartItem[];
  total: number;
  placedAt: string;
  customer: CheckoutDetails;
}

const PRODUCTS: Product[] = [
  { id: 1, name: 'Aero Street Runner', gender: 'Men', collection: 'Airflow', price: 450, img: '/static/airmax.jpg' },
  {
    id: 2,
    name: 'Pulse Knit Trainer',
    gender: 'Men',
    collection: 'Pulse',
    price: 390,
    img: '/static/reactinfinity.jpg',
  },
  {
    id: 3,
    name: 'Flash Carbon Racer',
    gender: 'Men',
    collection: 'Velocity',
    price: 599,
    img: '/static/zoomxvaporfly.jpg',
  },
  { id: 4, name: 'Cloud Grid Boost', gender: 'Men', collection: 'Cloudline', price: 420, img: '/static/ultraboost.jpg' },
  { id: 5, name: 'Metro Sock Runner', gender: 'Men', collection: 'Metro', price: 340, img: '/static/nmdr1.jpg' },
  { id: 6, name: 'Neon Rail Trainer', gender: 'Men', collection: 'Neon', price: 360, img: '/static/zx2kboost.jpg' },
  { id: 7, name: 'Retro Track Rider', gender: 'Men', collection: 'Retro', price: 260, img: '/static/futurerider.png' },
  { id: 8, name: 'Arcade Chunk Sneaker', gender: 'Men', collection: 'Arcade', price: 300, img: '/static/rsx.png' },
  {
    id: 9,
    name: 'Classic Court 574',
    gender: 'Men',
    collection: 'Classic',
    price: 370,
    img: '/static/newbalance574.png',
  },
  {
    id: 10,
    name: 'Foam Mile Cruiser',
    gender: 'Men',
    collection: 'Foam',
    price: 470,
    img: '/static/freshfoam1080.png',
  },
  { id: 11, name: 'Clean Court Low', gender: 'Women', collection: 'Classic', price: 400, img: '/static/airforce1.png' },
  {
    id: 12,
    name: 'Pegasus Pace Trainer',
    gender: 'Women',
    collection: 'Velocity',
    price: 350,
    img: '/static/pegasus.png',
  },
  {
    id: 13,
    name: 'Platform Canvas Lift',
    gender: 'Women',
    collection: 'Platform',
    price: 250,
    img: '/static/nizzaplatform.png',
  },
  {
    id: 14,
    name: 'Minimal Court Lace',
    gender: 'Women',
    collection: 'Court',
    price: 320,
    img: '/static/stansmith.png',
  },
  { id: 15, name: 'Cali Low Profile', gender: 'Women', collection: 'Coastal', price: 330, img: '/static/cali.png' },
  { id: 16, name: 'Mayfair Platform Sneaker', gender: 'Women', collection: 'Platform', price: 290, img: '/static/mayze.png' },
  { id: 17, name: 'City 327 Trainer', gender: 'Women', collection: 'Metro', price: 340, img: '/static/nb327.png' },
  {
    id: 18,
    name: 'Fuel Knit Runner',
    gender: 'Women',
    collection: 'Pulse',
    price: 420,
    img: '/static/fuelcellpropel.png',
  },
];

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  readonly products = PRODUCTS;
  readonly collections = ['All', ...Array.from(new Set(PRODUCTS.map((product) => product.collection))).sort()];
  readonly heroProduct = PRODUCTS[2];

  readonly activeSection = signal<Section>('home');
  readonly selectedCollection = signal('All');
  readonly toast = signal('');
  readonly checkoutOpen = signal(false);
  readonly checkoutError = signal('');
  readonly customerName = signal('');
  readonly customerEmail = signal('');
  readonly customerPhone = signal('');
  readonly customerAddress = signal('');
  readonly cart = signal<CartItem[]>(this.load<CartItem[]>('xmove-cart', []));
  readonly orders = signal<Order[]>(this.normalizeOrders(this.load<Order[]>('xmove-orders', [])));

  readonly visibleProducts = computed(() => {
    const gender: Gender = this.activeSection() === 'women' ? 'Women' : 'Men';
    const collection = this.selectedCollection();

    return this.products.filter(
      (product) => product.gender === gender && (collection === 'All' || product.collection === collection),
    );
  });

  readonly cartTotal = computed(() => this.cart().reduce((total, item) => total + item.price * item.qty, 0));

  showSection(section: Section): void {
    this.activeSection.set(section);
    if (section === 'men' || section === 'women') {
      this.checkoutOpen.set(false);
    }
  }

  setCollection(collection: string): void {
    this.selectedCollection.set(collection);
  }

  startShopping(gender: Gender): void {
    this.activeSection.set(gender === 'Men' ? 'men' : 'women');
  }

  addToCart(product: Product): void {
    const nextCart = [...this.cart()];
    const item = nextCart.find((cartItem) => cartItem.id === product.id);

    if (item) {
      item.qty += 1;
    } else {
      nextCart.push({ id: product.id, name: product.name, price: product.price, qty: 1 });
    }

    this.updateCart(nextCart);
    this.flash('Added to cart.');
  }

  orderNow(product: Product): void {
    this.addToCart(product);
    this.activeSection.set('cart');
    this.openCheckout();
  }

  updateQty(itemId: number, qty: string | number): void {
    const nextQty = Math.max(1, Number(qty) || 1);
    this.updateCart(this.cart().map((item) => (item.id === itemId ? { ...item, qty: nextQty } : item)));
  }

  removeItem(itemId: number): void {
    this.updateCart(this.cart().filter((item) => item.id !== itemId));
  }

  openCheckout(): void {
    if (this.cart().length === 0) {
      this.flash('Your cart is empty.');
      return;
    }

    this.checkoutError.set('');
    this.checkoutOpen.set(true);
  }

  closeCheckout(): void {
    this.checkoutOpen.set(false);
  }

  confirmOrder(): void {
    const customer = {
      name: this.customerName().trim(),
      email: this.customerEmail().trim(),
      phone: this.customerPhone().trim(),
      address: this.customerAddress().trim(),
    };

    if (!customer.name || !customer.email || !customer.phone || !customer.address) {
      this.checkoutError.set('Please complete all checkout details.');
      return;
    }

    const order: Order = {
      orderId: Date.now(),
      items: this.cart().map((item) => ({ ...item })),
      total: this.cartTotal(),
      placedAt: new Date().toLocaleString(),
      customer,
    };

    const nextOrders = [order, ...this.orders()];
    this.orders.set(nextOrders);
    this.save('xmove-orders', nextOrders);
    this.updateCart([]);
    this.checkoutOpen.set(false);
    this.activeSection.set('orders');
    this.customerName.set('');
    this.customerEmail.set('');
    this.customerPhone.set('');
    this.customerAddress.set('');
    this.flash('Order placed.');
  }

  cancelOrder(orderId: number): void {
    const nextOrders = this.orders().filter((order) => order.orderId !== orderId);
    this.orders.set(nextOrders);
    this.save('xmove-orders', nextOrders);
    this.flash('Order canceled.');
  }

  private updateCart(cart: CartItem[]): void {
    this.cart.set(cart);
    this.save('xmove-cart', cart);
  }

  private flash(message: string): void {
    this.toast.set(message);
    window.setTimeout(() => {
      if (this.toast() === message) {
        this.toast.set('');
      }
    }, 1800);
  }

  private load<T>(key: string, fallback: T): T {
    const value = localStorage.getItem(key);

    if (!value) {
      return fallback;
    }

    try {
      return JSON.parse(value) as T;
    } catch {
      return fallback;
    }
  }

  private save<T>(key: string, value: T): void {
    localStorage.setItem(key, JSON.stringify(value));
  }

  private normalizeOrders(orders: Order[]): Order[] {
    return orders.map((order) => ({
      ...order,
      customer: order.customer ?? {
        name: 'Guest customer',
        email: '',
        phone: 'Not provided',
        address: '',
      },
    }));
  }
}
