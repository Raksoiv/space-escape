'''
This module has useful methods to handle collisions
'''


def box_collide(left, right):
    assert hasattr(left, 'box_collider'), \
        f'{type(left).__name__} doesn\'t have a box collider'
    assert hasattr(right, 'box_collider'), \
        f'{type(right).__name__} doesn\'t have a box collider'

    return left.box_collider.colliderect(right.box_collider)
