import json

from fastapi import FastAPI, Request, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.backend.database import get_async_session

from app.backend.routers.v1.users import router as user_router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.backend.routers.v1.categories import get_all_cat, get_category_id
from app.backend.routers.v1.products import get_all_products
from app.backend.schemas.v1.users import UserFormSchemas
from app.backend.security.guest_user import GuestUserMiddleware
from app.backend.service.v1.users import UsersService, ProdUserService
from app.backend.routers.v1.users import get_count_user_prod, get_prod_user
from app.backend.routers.v1.cover_photo import get_photos
from app.backend.service.v1.cover_photo import CoverPhotoService
from app.backend.service.v1.popular_products import PopularProductsService
from app.backend.service.v1.products import CategoriesService
from app.backend.schemas.v1.products import CategoriesSchemas
from app.backend.schemas.v1.products import ProductsSchemas
from app.backend.service.v1.products import ProductsService
from app.backend.security.auth import router as auth_router
from app.backend.security.auth import protected_page
from app.backend.routers.v1.popular_products import get_all_popular_products
from app.backend.tg_bot import send_msg
from app.backend.service.v1.order import get_product_for_order


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")
app.add_middleware(GuestUserMiddleware)
app.include_router(user_router)
app.include_router(auth_router)


templates = Jinja2Templates(directory="app/frontend")


@app.get("/auth", response_class=HTMLResponse, response_model=None)
async def auth(
    request: Request,
):
    return templates.TemplateResponse(
        request=request, name="auth.html"
    )


@app.post('/user_form')
async def get_user_form(
        body: UserFormSchemas = Form()
):

    await send_msg(value=f'Новая заявка:\n\n'
                         f'Повод: {body.occasion}\n'
                         f'Дата: {body.date}\n'
                         f'Бюджет: {body.price}р\n'
                         f'Номер заказчика: {body.number}')
    return RedirectResponse(url='/', status_code=303)


@app.get("/", response_class=HTMLResponse)
async def catalog(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        cat=Depends(get_all_cat),
        popular_prod=Depends(get_all_popular_products),
        counts=Depends(get_count_user_prod),
):

    response = templates.TemplateResponse(
        request=request,
        name="main.html",
        context={
            'categories': cat,
            'popular_prod': popular_prod,
            'counts': counts,

        }
    )

    await UsersService.add_users(
        request=request,
        session=session,
        response=response
    )

    return response


@app.get(
    "/categories/{id}/products",
    response_class=HTMLResponse
)
async def catalog(
        response: Response,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        categories=Depends(get_all_cat),
        category=Depends(get_category_id),
        products=Depends(get_all_products),
        counts=Depends(get_count_user_prod)

):
    await UsersService.add_users(
        request=request,
        session=session,
        response=response,
    )
    return templates.TemplateResponse(
        request=request,
        name="catalog.html",
        context={
            'categories': categories,
            'products': products,
            'cate': category,
            'counts': counts
        }
    )


@app.get('/contacts')
async def get_contacts(
        response: Response,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        categories=Depends(get_all_cat),
        counts=Depends(get_count_user_prod)
):
    await UsersService.add_users(
        request=request,
        session=session,
        response=response
    )
    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={'categories': categories, 'counts': counts}
    )


@app.get('/delivery')
async def get_delivery(
        response: Response,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        categories=Depends(get_all_cat),
        counts=Depends(get_count_user_prod)
):
    await UsersService.add_users(
        request=request,
        session=session,
        response=response,
    )
    return templates.TemplateResponse(
        request=request,
        name="delivery.html",
        context={'categories': categories, 'counts': counts}
    )


@app.get('/profile')
async def get_profile(
        response: Response,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        categories=Depends(get_all_cat),
        counts=Depends(get_count_user_prod),
        prod_user=Depends(get_prod_user)
):
    await UsersService.add_users(
        request=request,
        session=session,
        response=response
    )
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={'categories': categories, 'counts': counts, 'prod_user': prod_user},

    )


@app.post('/profile/products/delete/{id}')
async def delete_in_my_favorites(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    return await ProdUserService.delete_prod_in_favorites(
        id=id,
        session=session
    )


@app.post("/order")
async def create_order(
        name: str = Form(),
        phone: str = Form(),
        session: AsyncSession = Depends(get_async_session),
        products: str = Form(...)
):
    products_list = json.loads(products)
    product_list_in_tg = []

    for i in products_list:
        result = await get_product_for_order(id=int(i), session=session)

        # Добавляем название и цену каждого товара
        product_name = result[0]['Products'].name
        product_price = result[0]['Products'].price

        # Форматируем строку для каждого товара
        product_list_in_tg.append(f"{product_name} - {product_price}₽")

    # Добавляем данные пользователя
    product_list_in_tg.append(f"Имя: {name}")
    product_list_in_tg.append(f"Телефон: {phone}")

    # Теперь собираем все данные в одно сообщение
    message = "Новая заявка\n" + "\n".join(product_list_in_tg)
    await send_msg(value=message)

    for prod in products_list:
        await ProdUserService.delete_prod_in_favorites(
            session=session,
            id=int(prod)
        )
    return RedirectResponse(url='/', status_code=303)


@app.get('/admin')
async def get_admin_panel(
        request: Request,
        photo=Depends(get_photos),
        popular_products=Depends(get_all_popular_products),
        categories=Depends(get_all_cat),
        product=Depends(get_all_products),
        protected=Depends(protected_page),

):
    if protected:
        return templates.TemplateResponse(
            request=request,
            name="admin.html",
            context={
                'photos': photo,
                'popular_products': popular_products,
                'categories': categories,
                'products': product
            }
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.post('/admin/cover/{id}/update')
async def update_cover(
        id: int,
        url: str = Form(),
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),

):
    if protected:
        await CoverPhotoService.update_photo_cover(
            id=id,
            session=session,
            url=url
        )
        return RedirectResponse(url='/admin', status_code=303)
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.get('/admin/cover/{id}')
async def get_cover(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        cover = await CoverPhotoService.get_cover_photo_id(
            id=id,
            session=session
        )
        return templates.TemplateResponse(
            request=request,
            name="cover.html",
            context={'covers': cover}
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.post('/admin/products/add')
async def add_product(
        body: ProductsSchemas = Form(),
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        await ProductsService.add_products(
            body=body,
            session=session,
        )
        return RedirectResponse(url='/admin', status_code=303)
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.get('/admin/products/{id}')
async def get_product(
        request: Request,
        id: int,
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        product = await ProductsService.get_product(
            id=id,
            session=session
        )
        return templates.TemplateResponse(
            request=request,
            name="product.html",
            context={'products': product}
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.post('/admin/products/{id}/update')
async def add_product(
        id: int,
        name: str | None = Form(None),
        descriptions: str | None = Form(None),
        price: int | None = Form(None),
        old_price: int | None = Form(None),
        url_photo: str | None = Form(None),
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        await ProductsService.update_products(
            name=name,
            descriptions=descriptions,
            price=price,
            old_price=old_price,
            url_photo=url_photo,
            id=id,
            session=session,
        )
        return RedirectResponse(url='/admin', status_code=303)
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.post('/admin/products/{id}/delete')
async def add_product(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        await ProductsService.delete_product(
            id=id,
            session=session,
        )
        return RedirectResponse(url='/admin', status_code=303)
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.post('/admin/categories/add')
async def add_category(
        body: CategoriesSchemas = Form(),
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        await CategoriesService.add_categories(
            body=body,
            session=session,
        )
        return RedirectResponse(url='/admin', status_code=303)
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.post('/admin/categories/{id}/delete')
async def delete_category(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        await CategoriesService.delete_cat(
            id=id,
            session=session,
        )
        return RedirectResponse(url='/admin', status_code=303)
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.get('/admin/categories/{id}')
async def get_category(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        categories = await CategoriesService.get_category(
            id=id,
            session=session
        )
        return templates.TemplateResponse(
            request=request,
            name="categories.html",
            context={'categories': categories}
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.post('/admin/categories/{id}/update')
async def get_category(
        id: int,
        name: str = Form(),
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        await CategoriesService.update_category(
            id=id,
            session=session,
            name=name
        )
        return RedirectResponse(url='/admin', status_code=303)
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.post('/admin/popular_products/{id}/update')
async def update_popular_product(
        id: int,
        name: str | None = Form(None),
        descriptions: str | None = Form(None),
        price: int | None = Form(None),
        old_price: int | None = Form(None),
        url_photo: str | None = Form(None),
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        await PopularProductsService.path_popular_product(
            id=id,
            session=session,
            name=name,
            descriptions=descriptions,
            price=price,
            old_price=old_price,
            url_photo=url_photo
        )
        return RedirectResponse(url='/admin', status_code=303)
    else:
        return RedirectResponse(url='/auth', status_code=303)


@app.get('/admin/popular_product/{id}')
async def get_popular_products(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        protected=Depends(protected_page),
):
    if protected:
        popular_products = await PopularProductsService.get_popular_product_id(
            id=id,
            session=session
        )
        return templates.TemplateResponse(
            request=request,
            name="popular_product.html",
            context={'popular_products': popular_products}
        )
    else:
        return RedirectResponse(url='/auth', status_code=303)

