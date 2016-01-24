package TestProject;


import TestProject.Item.testitem;
import net.minecraft.item.Item;
import TestProject.Block.testblock;
import net.minecraft.block.Block;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.Mod.Instance;
import net.minecraftforge.fml.common.SidedProxy;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.registry.EntityRegistry;
import net.minecraftforge.fml.common.registry.GameRegistry;
import net.minecraft.entity.EntityList;
import net.minecraft.item.Item;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraft.client.renderer.entity.RenderItem;
import net.minecraft.client.Minecraft;
import net.minecraft.client.resources.model.ModelResourceLocation;

@Mod(modid = TestProject.MODID, name = "TestProject", version = TestProject.VERSION)

public class TestProject {

    public static final String MODID = "testproject";
    public static final String VERSION = "1.0";
    
    @Instance(MODID)
    public static TestProject instance;
    
    


    //declarations
        public static Item testitem_Instance;
    public static Block testblock_Instance;
   
    public static void registerEntity(Class entityClass, int entityID, String name) {
        EntityRegistry.registerGlobalEntityID(entityClass, name, entityID);
    }
    
    public static void registerSpawnEgg(int entityID, int primaryColor, int secondaryColor) {
        EntityList.entityEggs.put(Integer.valueOf(entityID), new EntityList.EntityEggInfo(entityID, primaryColor, secondaryColor));
    }
	
	
	@EventHandler
	public void preInit(FMLPreInitializationEvent event) {

	}

	@EventHandler
	public void init(FMLInitializationEvent event) {
testitem_Instance = new testitem();
testblock_Instance = new testblock();
		if (event.getSide() == Side.CLIENT) {
			RenderItem renderItem = Minecraft.getMinecraft().getRenderItem();
			        renderItem.getItemModelMesher().register(testitem_Instance, 0, new ModelResourceLocation("testproject:testitem", "inventory"));
		}
	}

	@EventHandler
	public static void postInit(FMLPostInitializationEvent event) {

	}
}