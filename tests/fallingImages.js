var myBlogScale = 1 / PTM * 0.54 // 图片像素跟body比例倍数
var myBlogJson = {}
var myBlogImages = new Map(); // 图片缓存

var groundBody;

var embox2dTest_fallingImages = function() {
}

embox2dTest_fallingImages.prototype.setNiceViewCenter = function() {
    PTM = 32;
    setViewCenterWorld( new b2Vec2(0,0), true );
}

embox2dTest_fallingImages.prototype.setup = function() {

    var NUMRANGE = [];    
    // while (NUMRANGE.length < 10)
    //     NUMRANGE.push(NUMRANGE.length+1);
    bodies = [null]; // Indexes start from 1
    
    var bd_ground = new b2BodyDef();
    groundBody = world.CreateBody(bd_ground);

    var w2 = CW / 2 / PTM;
    var h2 = CH / 2 / PTM - 1;
    //ground edges
    var shape0 = new b2EdgeShape();
    shape0.Set(new b2Vec2(-w2, -h2), new b2Vec2(w2, -h2)); // bottom
    groundBody.CreateFixture(shape0, 0.0);
    shape0.Set(new b2Vec2(-w2, -h2), new b2Vec2(-w2, h2 * 10)); // left
    groundBody.CreateFixture(shape0, 0.0);
    shape0.Set(new b2Vec2(w2, -h2), new b2Vec2(w2, h2 * 10)); // right
    groundBody.CreateFixture(shape0, 0.0);


    var cshape = new b2CircleShape();
    cshape.set_m_radius(0.5);

    //falling shapes
    var ZERO = new b2Vec2(0, 0);
    var temp = new b2Vec2(0, 0);
    NUMRANGE.forEach(function(i) {
        var bd = new b2BodyDef();
        // bd.set_type(b2_dynamicBody);
        bd.set_type(Module.b2_dynamicBody);
        bd.set_position(ZERO);
        var body = world.CreateBody(bd);
        var randomValue = Math.random();
        if ( randomValue < 0.2 )
            body.CreateFixture(cshape, 1.0);
        else
            body.CreateFixture(createRandomPolygonShape(0.5), 1.0);
        temp.Set(16*(Math.random()-0.5), 4.0 + 2.5*i);
        body.SetTransform(temp, 0.0);
        body.SetLinearVelocity(ZERO);
        body.SetAwake(1);
        body.SetActive(1);
    });

    // //static polygon and chain shapes
    // {
    //     var verts = [];
    //     verts.push( new b2Vec2( 7,-1) );
    //     verts.push( new b2Vec2( 8,-2) );
    //     verts.push( new b2Vec2( 9, 3) );
    //     verts.push( new b2Vec2( 7, 1) );
    //     var polygonShape = createPolygonShape(verts);
    //     groundBody.CreateFixture(polygonShape, 0.0);
        
    //     //mirror vertices in x-axis and use for chain shape
    //     for (var i = 0; i < verts.length; i++)
    //         verts[i].set_x( -verts[i].get_x() );
    //     verts.reverse();
    //     var chainShape = createChainShape(verts, true);//true for closed loop *** some problem with this atm
    //     // polygonShape = createPolygonShape(verts);
    //     groundBody.CreateFixture(chainShape, 0.0);
    // }

    initMyBlog('images/json.txt')
}

function addImageBody(id) {
    var image = new Image()
    image.src = myBlogJson[id]['path']
    image.onload = function() {
        var w = image.width * myBlogScale
        var h = image.height * myBlogScale
        var ZERO = new b2Vec2(0, 0);
        var temp = new b2Vec2(0, 0);
        var bd = new b2BodyDef();
        // bd.set_type(b2_dynamicBody);
        bd.set_type(Module.b2_dynamicBody);
        bd.set_position(ZERO);
        var body = world.CreateBody(bd);
        var randomValue = Math.random();

        // if (id == 753) {
        //     var shape = new b2CircleShape();
        //     console.log(shape);
        //     shape.set_m_radius(w / 2);
        //     body.CreateFixture(shape, 1);
        // } else {
            var shape = new b2PolygonShape();
            shape.SetAsBox(w / 2, h / 2);
            body.CreateFixture(shape, 1);
        // }

        // 标题用几个DistanceJoint固定在页面上方，有一定弹性
        if (id == 1) {
            var def = new b2DistanceJointDef();
            def.collideConnected = false;
            def.frequencyHz = 2;
            def.dampingRatio = 1;
            def.length = 0;
            def.bodyA = groundBody;
            def.bodyB = body;
            def.localAnchorA.x = -1;
            def.localAnchorA.y = 10;
            def.localAnchorB.x = -1;
            def.localAnchorB.y = 0;
            world.CreateJoint(def);

            def.localAnchorA.x = 1;
            def.localAnchorB.x = 1;
            world.CreateJoint(def);

            def.localAnchorA.x = 0;
            def.localAnchorB.y = 1;
            world.CreateJoint(def);
        }
        
        temp.Set(22*(Math.random()-0.5), 12);
        body.SetTransform(temp, 0.0);
        body.SetLinearVelocity(ZERO);
        // body.SetAngle
        body.SetAwake(1);
        body.SetActive(1);

        body.SetUserData(id);
        myBlogImages.set(id, image)
    }
}

function initMyBlog(file) {
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                handleJsonStr(allText);
            }
        }
    }
    rawFile.send(null);
}

function handleJsonStr(str) {
    var json = JSON.parse(str);
    for (i = 0; i < json.length; i++) {
        var data = json[i];
        var id = data['id']
        allId.push(id);
        myBlogJson[id] = data
    }

    addOne();
}

function addOne() {
    if (allIdIndex < allId.length) {
        var id = allId[allIdIndex++];
        addImageBody(id);
        setTimeout(() => {
            addOne();
        }, 50);
    }
}

var allId = []
var allIdIndex = 0