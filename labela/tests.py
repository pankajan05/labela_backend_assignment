from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import CartItem, User, Cart, Product
from django.urls import reverse

class CartItemAPITestCase(TestCase):
    def setUp(self):
        # Create a test user (You may need to adjust this based on your User model)
        self.user = User.objects.create(username='testuser', password='testpassword')
        
        # Create a test cart
        self.cart = Cart.objects.create(user=self.user)
        
         # Create test products
        self.product1 = Product.objects.create(name='Product 1', rating=5, description='Description 1', price=10.99)
        self.product2 = Product.objects.create(name='Product 2', rating=4, description='Description 2', price=19.99)
        self.product3 = Product.objects.create(name='Product 3', rating=3, description='Description 3', price=7.99)
        
        # Create test cart items
        self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

        # Initialize the test client
        self.client = APIClient()
        
        # Log in the test user (You may need to adjust this based on your authentication setup)
        self.client.login(username='testuser', password='testpassword')
        
    def test_list_cartitems(self):
        url = reverse('cartitem-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming you have two test cart items
        
    def test_create_cartitem(self):
        url = reverse('cartitem-list-create')
        data = {'cart': self.cart.id, 'product': self.product3.id, 'quantity': 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 3)  # Assuming you created 2 items in setUp()

    def test_retrieve_cartitem(self):
        url = reverse('cartitem-retrieve-update-destroy', kwargs={'pk': self.cart_item1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 2)

    def test_update_cartitem(self):
        url = reverse('cartitem-retrieve-update-destroy', kwargs={'pk': self.cart_item1.id})
        data = {'quantity': 4, 'cart': self.cart.id, 'product': self.product3.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_item1.refresh_from_db()
        self.assertEqual(self.cart_item1.quantity, 4)

    def test_delete_cartitem(self):
        url = reverse('cartitem-retrieve-update-destroy', kwargs={'pk': self.cart_item1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item1.id).exists())
